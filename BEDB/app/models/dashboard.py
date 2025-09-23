"""Dashboard progress model."""

from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId


class ProgressStatus(str, Enum):
    """Progress status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class DashboardProgress(Document):
    """Dashboard progress document model."""
    
    user_id: ObjectId = Field(..., index=True)
    course_id: ObjectId = Field(..., index=True)
    chapter_id: Optional[ObjectId] = Field(None, index=True)
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    progress: float = Field(default=0.0, ge=0.0, le=100.0)  # Percentage
    time_spent: int = Field(default=0)  # Time in minutes
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "dashboard_progress"
        indexes = [
            "user_id",
            "course_id",
            "chapter_id",
            "status",
            "last_accessed"
        ]
    
    def __str__(self) -> str:
        return f"DashboardProgress(user_id={self.user_id}, course_id={self.course_id}, progress={self.progress})"
