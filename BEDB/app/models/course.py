"""Course and Chapter models."""

from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import Field

from app.models.base import BaseDocument, PyObjectId


class CourseLevel(str, Enum):
    """Course difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(BaseDocument):
    """Course document model."""
    
    class Settings:
        name = "courses"
    
    owner_id: PyObjectId = Field(..., index=True)
    title: str
    description: str
    outline: Optional[str] = None
    source: Optional[str] = None  # Source material or origin
    level: CourseLevel = CourseLevel.BEGINNER
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "courses"
        indexes = [
            "owner_id",
            "title",
            "level",
            "tags",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Course(title={self.title}, owner_id={self.owner_id})"


class Chapter(BaseDocument):
    """Chapter document model."""
    
    class Settings:
        name = "chapters"

    course_id: PyObjectId = Field(..., index=True)
    title: str
    content: str
    order: int = Field(..., index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "chapters"
        indexes = [
            "course_id",
            "order",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Chapter(title={self.title}, course_id={self.course_id}, order={self.order})"
