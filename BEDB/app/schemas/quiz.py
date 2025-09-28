"""Quiz related schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuizCreate(BaseModel):
    """Quiz creation schema."""
    course_id: str
    chapter_id: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    prompt: str = Field(..., min_length=1)


class QuizResponse(BaseModel):
    """Quiz response schema."""
    id: str
    course_id: str
    chapter_id: Optional[str] = None
    title: str
    prompt: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class QuizQuestionResponse(BaseModel):
    """Quiz question response schema."""
    id: str
    quiz_id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None
    order: int
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class QuizSubmission(BaseModel):
    """Quiz submission schema."""
    quiz_id: str
    answers: List[dict]  # List of {question_id: str, answer: int}


class QuizResult(BaseModel):
    """Quiz result schema."""
    quiz_id: str
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    answers: List[dict]
    taken_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }


class QuizHistoryResponse(BaseModel):
    """Quiz history response schema."""
    id: str
    quiz_id: str
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    taken_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            "ObjectId": str
        }
