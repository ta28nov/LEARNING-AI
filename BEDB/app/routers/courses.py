"""Course management endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, 
    ChapterCreate, ChapterUpdate, ChapterResponse
)
from app.models.course import Course, Chapter
from app.models.user import User
from app.auth import get_current_active_user
from app.services.genai_service import genai_service
from app.services.vector_service import vector_service
from app.utils import validate_object_id, safe_object_id_conversion
from bson import ObjectId

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new course."""
    course = Course(
        owner_id=current_user.id,
        title=course_data.title,
        description=course_data.description,
        outline=course_data.outline,
        source=course_data.source,
        level=course_data.level,
        tags=course_data.tags
    )
    
    await course.insert()
    
    # Index course content for vector search
    await vector_service.index_course_content(str(course.id))
    
    return CourseResponse.model_validate(course)


@router.post("/from-prompt", response_model=CourseResponse)
async def create_course_from_prompt(
    topic: str,
    level: str = "beginner",
    current_user: User = Depends(get_current_active_user)
):
    """Create a course from a topic prompt using AI."""
    try:
        # Generate course outline using AI
        outline = await genai_service.generate_course_outline(topic, level)
        
        # Create course
        course = Course(
            owner_id=current_user.id,
            title=f"AI Generated Course: {topic}",
            description=f"An AI-generated course about {topic}",
            outline=outline,
            source="AI Generated",
            level=level,
            tags=[topic.lower(), "ai-generated"]
        )
        
        await course.insert()
        
        # Index course content for vector search
        await vector_service.index_course_content(str(course.id))
        
        return CourseResponse.model_validate(course)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create course from prompt: {str(e)}"
        )


@router.post("/from-upload")
async def create_course_from_upload(
    upload_id: str,
    title: str,
    metadata: dict = None,
    current_user: User = Depends(get_current_active_user)
):
    """Create a course from uploaded file."""
    try:
        # Get upload
        from app.models.upload import Upload
        upload = await Upload.get(ObjectId(upload_id))
        if not upload:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Upload not found"
            )
        
        if upload.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create course from this upload"
            )
        
        if not upload.extracted_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Upload has no extracted text content"
            )
        
        # Create course from upload content
        course = Course(
            owner_id=current_user.id,
            title=title,
            description=f"Course generated from upload: {upload.filename}",
            outline=upload.extracted_text[:1000] + "..." if len(upload.extracted_text) > 1000 else upload.extracted_text,
            source="Upload",
            level="beginner",
            tags=["upload-generated", upload.file_type]
        )
        await course.insert()
        
        # Index course content
        await vector_service.index_course_content(str(course.id))
        
        return {"job_id": str(course.id)}  # Return as job_id for async processing
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create course from upload: {str(e)}"
        )


@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    owner: str = Query("user", description="Filter by owner: 'user' or 'system'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get courses based on owner filter."""
    if owner == "user":
        courses = await Course.find(
            Course.owner_id == current_user.id
        ).skip(skip).limit(limit).to_list()
    elif owner == "system":
        # Get system/sample courses (you can define criteria for system courses)
        courses = await Course.find(
            Course.owner_id != current_user.id
        ).skip(skip).limit(limit).to_list()
    else:
        # Get all courses user has access to
        courses = await Course.find().skip(skip).limit(limit).to_list()
    
    return [CourseResponse.model_validate(course) for course in courses]


@router.get("/public", response_model=List[CourseResponse])
async def get_public_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    level: Optional[str] = None,
    tags: Optional[List[str]] = Query(None)
):
    """Get public courses (sample courses)."""
    query = {}
    if level:
        query["level"] = level
    if tags:
        query["tags"] = {"$in": tags}
    
    courses = await Course.find(query).skip(skip).limit(limit).to_list()
    return [CourseResponse.model_validate(course) for course in courses]


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific course."""
    try:
        obj_id = validate_object_id(course_id, "course ID")
        course = await Course.get(obj_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Check if user owns the course or if it's public
        if course.owner_id != current_user.id:
            # For now, allow access to all courses
            # In production, you might want to implement proper access control
            pass
        
        return CourseResponse.model_validate(course)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a course."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this course"
            )
        
        # Update fields
        update_data = course_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(course, field, value)
        
        await course.save()
        
        # Re-index course content
        await vector_service.index_course_content(str(course.id))
        
        return CourseResponse.model_validate(course)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a course."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this course"
            )
        
        # Delete associated chapters
        await Chapter.find(Chapter.course_id == course.id).delete()
        
        # Delete course
        await course.delete()
        
        return {"message": "Course deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


# Chapter endpoints
@router.post("/{course_id}/chapters", response_model=ChapterResponse)
async def create_chapter(
    course_id: str,
    chapter_data: ChapterCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chapter for a course."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to add chapters to this course"
            )
        
        chapter = Chapter(
            course_id=course.id,
            title=chapter_data.title,
            content=chapter_data.content,
            order=chapter_data.order
        )
        
        await chapter.insert()
        
        # Index chapter content
        await vector_service.index_course_content(str(course.id))
        
        return ChapterResponse.model_validate(chapter)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.get("/{course_id}/chapters", response_model=List[ChapterResponse])
async def get_chapters(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get chapters for a course."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        chapters = await Chapter.find(
            Chapter.course_id == course.id
        ).sort("order").to_list()
        
        return [ChapterResponse.model_validate(chapter) for chapter in chapters]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.get("/{course_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    course_id: str,
    chapter_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific chapter."""
    try:
        chapter = await Chapter.get(ObjectId(chapter_id))
        if not chapter or str(chapter.course_id) != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        return ChapterResponse.model_validate(chapter)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )


@router.put("/{course_id}/chapters/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    course_id: str,
    chapter_id: str,
    chapter_data: ChapterUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update a chapter."""
    try:
        chapter = await Chapter.get(ObjectId(chapter_id))
        if not chapter or str(chapter.course_id) != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        # Check if user owns the course
        course = await Course.get(chapter.course_id)
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this chapter"
            )
        
        # Update fields
        update_data = chapter_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(chapter, field, value)
        
        await chapter.save()
        
        # Re-index course content
        await vector_service.index_course_content(str(course.id))
        
        return ChapterResponse.model_validate(chapter)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )


@router.delete("/{course_id}/chapters/{chapter_id}")
async def delete_chapter(
    course_id: str,
    chapter_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete a chapter."""
    try:
        chapter = await Chapter.get(ObjectId(chapter_id))
        if not chapter or str(chapter.course_id) != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        # Check if user owns the course
        course = await Course.get(chapter.course_id)
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this chapter"
            )
        
        await chapter.delete()
        
        # Re-index course content
        await vector_service.index_course_content(str(course.id))
        
        return {"message": "Chapter deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )


@router.post("/{course_id}/generate-outline")
async def generate_course_outline(
    course_id: str,
    prompt: str,
    current_user: User = Depends(get_current_active_user)
):
    """Generate course outline using AI."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if course.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this course"
            )
        
        # Generate outline using AI
        outline = await genai_service.generate_course_outline(prompt, course.level)
        
        return {"outline": outline}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate outline: {str(e)}"
        )


@router.post("/{course_id}/chat")
async def chat_with_course(
    course_id: str,
    message: str,
    mode: str = "hybrid",
    current_user: User = Depends(get_current_active_user)
):
    """Chat with AI in course context."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Get course content for context
        chapters = await Chapter.find(Chapter.course_id == course.id).to_list()
        content = course.description + "\n\n"
        
        for chapter in chapters:
            content += f"Chapter {chapter.order}: {chapter.title}\n{chapter.content}\n\n"
        
        # Get relevant context using vector search
        context = await vector_service.get_relevant_context(
            query=message,
            course_id=course_id
        )
        
        # Generate AI response
        from app.models.chat import ChatMode
        chat_mode = ChatMode.STRICT if mode == "strict" else ChatMode.HYBRID
        
        answer = await genai_service.chat_with_context(
            message=message,
            context=context or content,
            mode=chat_mode
        )
        
        return {
            "answer": answer,
            "source_context": context[:500] if context else None  # Truncate for response
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate response: {str(e)}"
        )


@router.post("/{course_id}/summarize")
async def summarize_chapter(
    course_id: str,
    chapter_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Generate summary for a chapter."""
    try:
        chapter = await Chapter.get(ObjectId(chapter_id))
        if not chapter or str(chapter.course_id) != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        # Generate summary using AI
        summary = await genai_service.generate_summary(chapter.content)
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}"
        )


@router.post("/{course_id}/flashcards")
async def generate_flashcards(
    course_id: str,
    chapter_id: str,
    num_cards: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """Generate flashcards for a chapter."""
    try:
        chapter = await Chapter.get(ObjectId(chapter_id))
        if not chapter or str(chapter.course_id) != course_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chapter not found"
            )
        
        # Generate flashcards using AI
        flashcards = await genai_service.generate_flashcards(chapter.content, num_cards)
        
        return flashcards
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate flashcards: {str(e)}"
        )
