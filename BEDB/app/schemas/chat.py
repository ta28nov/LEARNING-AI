"""Chat related schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.chat import ChatMode, ChatStatus


class ChatSessionCreate(BaseModel):
    """Chat session creation schema."""
    course_id: Optional[str] = None
    upload_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    mode: ChatMode = ChatMode.HYBRID


class ChatSessionResponse(BaseModel):
    """Chat session response schema."""
    id: str
    user_id: str
    course_id: Optional[str] = None
    upload_id: Optional[str] = None
    title: str
    mode: ChatMode
    status: ChatStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class ChatMessageCreate(BaseModel):
    """Chat message creation schema."""
    message: str = Field(..., min_length=1, max_length=2000)


class ChatMessageResponse(BaseModel):
    """Chat message response schema."""
    id: str
    session_id: str
    sender: str
    message: str
    answer: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class ChatResponse(BaseModel):
    """Chat response schema."""
    message: str
    answer: str
    metadata: Optional[dict] = None
