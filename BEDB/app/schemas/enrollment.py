"""Course enrollment and progress schemas."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Enrollment Schemas
class CourseEnrollRequest(BaseModel):
    """Request schema for course enrollment."""
    pass  # No additional data needed, just the course_id from URL


class CourseEnrollmentResponse(BaseModel):
    """Response schema for course enrollment."""
    id: str
    student_id: str
    course_id: str
    enrolled_at: datetime
    status: str
    progress: float
    last_accessed: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Chapter Progress Schemas
class ChapterProgressUpdate(BaseModel):
    """Schema for updating chapter progress."""
    status: Optional[str] = None
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    time_spent: Optional[int] = Field(None, ge=0)  # minutes
    notes: Optional[str] = None


class ChapterProgressResponse(BaseModel):
    """Response schema for chapter progress."""
    id: str
    user_id: str
    chapter_id: str
    course_id: str
    status: str
    progress: float
    time_spent: int
    last_accessed: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


# Course Visibility Update
class CourseVisibilityUpdate(BaseModel):
    """Schema for updating course visibility."""
    visibility: str = Field(..., pattern="^(public|private|draft)$")


# Student Dashboard Schemas
class EnrolledCourseInfo(BaseModel):
    """Schema for enrolled course information."""
    course_id: str
    title: str
    description: str
    level: str
    enrollment_status: str
    progress: float
    enrolled_at: datetime
    last_accessed: Optional[datetime] = None


class StudentDashboardResponse(BaseModel):
    """Schema for student dashboard response."""
    total_enrolled_courses: int
    completed_courses: int
    in_progress_courses: int
    total_time_spent: int  # minutes
    average_progress: float
    recent_courses: list[EnrolledCourseInfo]


# Instructor Dashboard Schemas
class StudentEnrollmentInfo(BaseModel):
    """Schema for student enrollment information in a course."""
    student_id: str
    student_name: str
    student_email: str
    enrolled_at: datetime
    progress: float
    status: str
    last_accessed: Optional[datetime] = None


class CourseAnalytics(BaseModel):
    """Schema for course analytics."""
    course_id: str
    title: str
    total_enrollments: int
    active_students: int
    completed_students: int
    average_progress: float
    average_time_spent: int  # minutes
    completion_rate: float


class InstructorDashboardResponse(BaseModel):
    """Schema for instructor dashboard response."""
    total_courses: int
    total_students: int
    total_enrollments: int
    average_course_rating: float
    recent_analytics: list[CourseAnalytics]
