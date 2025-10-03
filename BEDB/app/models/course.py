# course.py
from typing import Optional, List
from enum import Enum
from pydantic import Field
from datetime import datetime
from app.models.base import BaseDocument, PyObjectId


class CourseLevel(str, Enum):
    """Course difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseVisibility(str, Enum):
    """Course visibility types."""
    PUBLIC = "public"
    PRIVATE = "private"
    DRAFT = "draft"


class Course(BaseDocument):
    """Course document model."""
    
    owner_id: PyObjectId = Field(..., index=True)
    title: str
    description: str
    outline: Optional[str] = None
    source: Optional[str] = None
    level: CourseLevel = CourseLevel.BEGINNER
    tags: List[str] = Field(default_factory=list)
    visibility: CourseVisibility = CourseVisibility.DRAFT
    is_approved: bool = False
    approved_by: Optional[PyObjectId] = None
    approved_at: Optional[datetime] = None
    enrollment_count: int = 0
    
    class Settings:
        name = "courses"
        indexes = [
            "owner_id",
            "title",
            "level",
            "tags",
            "visibility",
            "is_approved",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Course(title={self.title}, owner_id={self.owner_id})"


class Chapter(BaseDocument):
    """Chapter document model."""
    
    course_id: PyObjectId = Field(..., index=True)
    title: str
    content: str
    order: int = Field(..., index=True)
    
    class Settings:
        name = "chapters"
        indexes = [
            "course_id",
            "order",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Chapter(title={self.title}, course_id={self.course_id}, order={self.order})"
