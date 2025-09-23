"""Course and Chapter models."""

from beanie import Document
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from bson import ObjectId


class CourseLevel(str, Enum):
    """Course difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(Document):
    """Course document model."""
    
    owner_id: ObjectId = Field(..., index=True)
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


class Chapter(Document):
    """Chapter document model."""
    
    course_id: ObjectId = Field(..., index=True)
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
