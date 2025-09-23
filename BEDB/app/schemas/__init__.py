"""Pydantic schemas for API requests and responses."""

from .auth import UserCreate, UserLogin, UserResponse, Token
from .course import CourseCreate, CourseUpdate, CourseResponse, ChapterCreate, ChapterResponse
from .upload import UploadResponse, UploadCreate
from .quiz import QuizCreate, QuizResponse, QuizQuestionResponse, QuizSubmission, QuizResult
from .chat import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse
from .dashboard import DashboardStats, ProgressUpdate

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "Token",
    "CourseCreate", "CourseUpdate", "CourseResponse", "ChapterCreate", "ChapterResponse",
    "UploadResponse", "UploadCreate",
    "QuizCreate", "QuizResponse", "QuizQuestionResponse", "QuizSubmission", "QuizResult",
    "ChatSessionCreate", "ChatSessionResponse", "ChatMessageCreate", "ChatMessageResponse",
    "DashboardStats", "ProgressUpdate"
]
