"""Dashboard related schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from app.models.dashboard import ProgressStatus


class ProgressUpdate(BaseModel):
    """Progress update schema."""
    course_id: str
    chapter_id: Optional[str] = None
    status: ProgressStatus
    progress: float = Field(..., ge=0.0, le=100.0)
    time_spent: int = Field(default=0, ge=0)


class DashboardStats(BaseModel):
    """Dashboard statistics schema."""
    total_courses: int
    completed_courses: int
    total_quizzes: int
    total_time_spent: int  # in minutes
    average_score: float
    recent_activity: List[dict]
    progress_by_course: List[dict]
    weekly_progress: List[dict]


class CourseProgress(BaseModel):
    """Course progress schema."""
    course_id: str
    course_title: str
    progress: float
    status: ProgressStatus
    time_spent: int
    last_accessed: datetime
    chapters_completed: int
    total_chapters: int
