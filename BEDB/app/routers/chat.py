"""Chat endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.chat import (
    ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, 
    ChatMessageResponse, ChatResponse
)
from app.models.chat import ChatSession, ChatMessage, ChatMode
from app.models.course import Course
from app.models.upload import Upload
from app.models.user import User
from app.auth import get_current_active_user
from app.services.genai_service import genai_service
from app.services.vector_service import vector_service
from bson import ObjectId

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chat session."""
    # Verify course exists if provided
    if session_data.course_id:
        course = await Course.get(ObjectId(session_data.course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
    
    # Verify upload exists if provided
    if session_data.upload_id:
        upload = await Upload.get(ObjectId(session_data.upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to use this upload"
            )
    
    # Create chat session
    session = ChatSession(
        user_id=current_user.id,
        course_id=ObjectId(session_data.course_id) if session_data.course_id else None,
        upload_id=ObjectId(session_data.upload_id) if session_data.upload_id else None,
        title=session_data.title,
        mode=session_data.mode
    )
    
    await session.insert()
    return ChatSessionResponse.model_validate(session)


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's chat sessions."""
    sessions = await ChatSession.find(
        ChatSession.user_id == current_user.id
    ).skip(skip).limit(limit).sort("-created_at").to_list()
    
    return [ChatSessionResponse.model_validate(session) for session in sessions]


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific chat session."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this chat session"
            )
        
        return ChatSessionResponse.model_validate(session)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get messages for a chat session."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this chat session"
            )
        
        messages = await ChatMessage.find(
            ChatMessage.session_id == session.id
        ).skip(skip).limit(limit).sort("created_at").to_list()
        
        return [ChatMessageResponse.model_validate(message) for message in messages]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )


@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
async def send_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Send a message in a chat session."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to send messages in this chat session"
            )
        
        # Save user message
        user_message = ChatMessage(
            session_id=session.id,
            sender="user",
            message=message_data.message
        )
        await user_message.insert()
        
        # Get context based on session mode and associated content
        context = None
        if session.mode == ChatMode.STRICT or session.mode == ChatMode.HYBRID:
            if session.course_id:
                context = await vector_service.get_relevant_context(
                    query=message_data.message,
                    course_id=str(session.course_id)
                )
            elif session.upload_id:
                context = await vector_service.get_relevant_context(
                    query=message_data.message,
                    upload_id=str(session.upload_id)
                )
        
        # Generate AI response
        try:
            ai_response = await genai_service.chat_with_context(
                message=message_data.message,
                context=context,
                mode=session.mode
            )
        except Exception as e:
            ai_response = f"Sorry, I encountered an error while processing your request: {str(e)}"
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=session.id,
            sender="ai",
            message=message_data.message,
            answer=ai_response
        )
        await ai_message.insert()
        
        return ChatResponse(
            message=message_data.message,
            answer=ai_response
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )


@router.post("/", response_model=ChatResponse)
async def freestyle_chat(
    message: str,
    mode: ChatMode = ChatMode.HYBRID,
    session_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
):
    """Freestyle chat without a session."""
    try:
        # Generate AI response
        ai_response = await genai_service.chat_with_context(
            message=message,
            context=None,
            mode=mode
        )
        
        return ChatResponse(
            message=message,
            answer=ai_response
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.post("/save")
async def save_chat_session(
    session_id: str,
    save_as: str,  # "course" or "note"
    current_user: User = Depends(get_current_active_user)
):
    """Save chat session as course or note."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to save this chat session"
            )
        
        if save_as == "course":
            # Get all messages from the session
            messages = await ChatMessage.find(
                ChatMessage.session_id == session.id
            ).sort("created_at").to_list()
            
            # Create course content from chat
            content = f"Course generated from chat session: {session.title}\n\n"
            for message in messages:
                if message.sender == "user":
                    content += f"Q: {message.message}\n"
                elif message.sender == "ai" and message.answer:
                    content += f"A: {message.answer}\n\n"
            
            # Create course
            from app.models.course import Course, CourseLevel
            course = Course(
                owner_id=current_user.id,
                title=f"Course from Chat: {session.title}",
                description=f"Course generated from chat session: {session.title}",
                outline=content,
                source="Chat Session",
                level=CourseLevel.BEGINNER,
                tags=["chat-generated", "ai-generated"]
            )
            await course.insert()
            
            return {"course_id": str(course.id)}
        else:
            # Save as note (simplified implementation)
            return {"note_id": str(session.id)}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )


@router.get("/history")
async def get_chat_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get chat history."""
    # Get recent chat messages across all sessions
    messages = await ChatMessage.find(
        ChatMessage.session_id.in_(
            [session.id for session in await ChatSession.find(
                ChatSession.user_id == current_user.id
            ).to_list()]
        )
    ).skip(skip).limit(limit).sort("-created_at").to_list()
    
    return [
        {
            "id": str(message.id),
            "message": message.message,
            "answer": message.answer,
            "created_at": message.created_at
        }
        for message in messages
    ]


@router.post("/{answer_id}/feedback")
async def submit_chat_feedback(
    answer_id: str,
    feedback: str,
    rating: int = None,
    current_user: User = Depends(get_current_active_user)
):
    """Submit feedback for a chat answer."""
    try:
        # Find the chat message
        message = await ChatMessage.get(ObjectId(answer_id))
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat message not found"
            )
        
        # Verify user has access to this message
        session = await ChatSession.get(message.session_id)
        if not session or session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to provide feedback for this message"
            )
        
        # Update message with feedback
        if not message.metadata:
            message.metadata = {}
        
        message.metadata["feedback"] = feedback
        if rating is not None:
            message.metadata["rating"] = rating
        
        await message.save()
        
        return {"message": "Feedback submitted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat message not found"
        )


@router.post("/sessions/{session_id}/save-as-course")
async def save_chat_as_course(
    session_id: str,
    course_title: str,
    current_user: User = Depends(get_current_active_user)
):
    """Save chat session as a new course."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to save this chat session"
            )
        
        # Get all messages from the session
        messages = await ChatMessage.find(
            ChatMessage.session_id == session.id
        ).sort("created_at").to_list()
        
        # Create course content from chat
        content = f"Course generated from chat session: {session.title}\n\n"
        for message in messages:
            if message.sender == "user":
                content += f"Q: {message.message}\n"
            elif message.sender == "ai" and message.answer:
                content += f"A: {message.answer}\n\n"
        
        # Create course
        from app.models.course import Course, CourseLevel
        course = Course(
            owner_id=current_user.id,
            title=course_title,
            description=f"Course generated from chat session: {session.title}",
            outline=content,
            source="Chat Session",
            level=CourseLevel.BEGINNER,
            tags=["chat-generated", "ai-generated"]
        )
        await course.insert()
        
        # Index course content
        await vector_service.index_course_content(str(course.id))
        
        return {"message": "Chat session saved as course", "course_id": str(course.id)}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )


@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a chat session."""
    try:
        session = await ChatSession.get(ObjectId(session_id))
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this chat session"
            )
        
        # Delete all messages in the session
        await ChatMessage.find(ChatMessage.session_id == session.id).delete()
        
        # Delete the session
        await session.delete()
        
        return {"message": "Chat session deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
