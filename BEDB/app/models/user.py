"""User model."""

from beanie import Document
from pydantic import EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles."""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


class User(Document):
    """User document model."""
    
    email: EmailStr = Field(..., unique=True, index=True)
    password_hash: str
    name: str
    avatar: Optional[str] = None
    role: UserRole = UserRole.STUDENT
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "created_at",
            "is_active"
        ]
    
    def __str__(self) -> str:
        return f"User(email={self.email}, name={self.name})"
