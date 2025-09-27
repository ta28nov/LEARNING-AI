"""Quiz related models."""

from beanie import Document
from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.models.base import PyObjectId


class Quiz(Document):
    """Quiz document model."""
    
    course_id: PyObjectId = Field(..., index=True)
    chapter_id: Optional[PyObjectId] = Field(None, index=True)
    title: str
    prompt: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "quizzes"
        indexes = [
            "course_id",
            "chapter_id",
            "created_at"
        ]
    
    def __str__(self) -> str:
        return f"Quiz(title={self.title}, course_id={self.course_id})"


class QuizQuestion(Document):
    """Quiz question document model."""
    
    quiz_id: PyObjectId = Field(..., index=True)
    question: str
    options: List[str] = Field(default_factory=list)
    correct_answer: int  # Index of correct option
    explanation: Optional[str] = None
    order: int = Field(default=0)
    
    class Settings:
        name = "quiz_questions"
        indexes = [
            "quiz_id",
            "order"
        ]
    
    def __str__(self) -> str:
        return f"QuizQuestion(quiz_id={self.quiz_id}, order={self.order})"


class QuizHistory(Document):
    """Quiz history document model."""
    
    quiz_id: PyObjectId = Field(..., index=True)
    user_id: PyObjectId = Field(..., index=True)
    score: float  # Percentage score
    total_questions: int
    correct_answers: int
    answers: List[dict] = Field(default_factory=list)  # User's answers
    taken_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "quiz_history"
        indexes = [
            "quiz_id",
            "user_id",
            "taken_at"
        ]
    
    def __str__(self) -> str:
        return f"QuizHistory(quiz_id={self.quiz_id}, user_id={self.user_id}, score={self.score})"
