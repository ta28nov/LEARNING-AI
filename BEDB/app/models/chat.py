"""Chat related models."""

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId


class ChatMode(str, Enum):
    """Chat session modes."""
    STRICT = "strict"  # Only use uploaded/course data
    HYBRID = "hybrid"  # Combine user data + Gemini knowledge


class ChatStatus(str, Enum):
    """Chat session status."""
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class ChatSession(Document):
    """Chat session document model."""
    
    user_id: ObjectId = Field(..., index=True)
    course_id: Optional[ObjectId] = Field(None, index=True)
    upload_id: Optional[ObjectId] = Field(None, index=True)
    title: str
    mode: ChatMode = ChatMode.HYBRID
    status: ChatStatus = ChatStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "chat_sessions"
        indexes = [
            "user_id",
            "course_id",
            "upload_id",
            "status",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"ChatSession(title={self.title}, user_id={self.user_id}, mode={self.mode})"


class ChatMessage(Document):
    """Chat message document model."""
    
    session_id: ObjectId = Field(..., index=True)
    sender: str  # "user" or "ai"
    message: str
    answer: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "chat_messages"
        indexes = [
            "session_id",
            "sender",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"ChatMessage(session_id={self.session_id}, sender={self.sender})"
