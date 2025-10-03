"""Course enrollment and progress models."""

from typing import Optional
from enum import Enum
from pydantic import Field
from datetime import datetime
from app.models.base import BaseDocument, PyObjectId


class EnrollmentStatus(str, Enum):
    """Enrollment status types."""
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"


class CourseEnrollment(BaseDocument):
    """Course enrollment document model."""
    
    student_id: PyObjectId = Field(..., index=True)
    course_id: PyObjectId = Field(..., index=True)
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    last_accessed: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Settings:
        name = "course_enrollments"
        indexes = [
            "student_id",
            "course_id",
            [("student_id", 1), ("course_id", 1)],  # Compound index for unique constraint
            "enrolled_at",
            "status"
        ]
    
    def __str__(self) -> str:
        return f"CourseEnrollment(student_id={self.student_id}, course_id={self.course_id}, status={self.status})"


class ChapterProgressStatus(str, Enum):
    """Chapter progress status types."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ChapterProgress(BaseDocument):
    """Chapter progress tracking document model."""
    
    user_id: PyObjectId = Field(..., index=True)
    chapter_id: PyObjectId = Field(..., index=True)
    course_id: PyObjectId = Field(..., index=True)
    status: ChapterProgressStatus = ChapterProgressStatus.NOT_STARTED
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    time_spent: int = Field(default=0)  # in minutes
    last_accessed: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    
    class Settings:
        name = "chapter_progress"
        indexes = [
            "user_id",
            "chapter_id",
            "course_id",
            [("user_id", 1), ("chapter_id", 1)],  # Compound index for unique constraint
            [("user_id", 1), ("course_id", 1)],
            "status",
            "last_accessed"
        ]
    
    def __str__(self) -> str:
        return f"ChapterProgress(user_id={self.user_id}, chapter_id={self.chapter_id}, status={self.status})"
