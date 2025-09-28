"""Course related schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.course import CourseLevel


class CourseCreate(BaseModel):
    """Course creation schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    outline: Optional[str] = None
    source: Optional[str] = None
    level: CourseLevel = CourseLevel.BEGINNER
    tags: List[str] = Field(default_factory=list)


class CourseUpdate(BaseModel):
    """Course update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    outline: Optional[str] = None
    source: Optional[str] = None
    level: Optional[CourseLevel] = None
    tags: Optional[List[str]] = None


class CourseResponse(BaseModel):
    """Course response schema."""
    id: str
    owner_id: str
    title: str
    description: str
    outline: Optional[str] = None
    source: Optional[str] = None
    level: CourseLevel
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class ChapterCreate(BaseModel):
    """Chapter creation schema."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    order: int = Field(..., ge=1)


class ChapterUpdate(BaseModel):
    """Chapter update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    order: Optional[int] = Field(None, ge=1)


class ChapterResponse(BaseModel):
    """Chapter response schema."""
    id: str
    course_id: str
    title: str
    content: str
    order: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }
