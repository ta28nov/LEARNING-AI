"""Database connection and initialization."""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.models import (
    User, Course, Upload, Quiz, QuizQuestion, Chapter,
    QuizHistory, DashboardProgress, ChatSession, ChatMessage
)


async def init_db():
    """Initialize database connection and Beanie ODM."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    
    await init_beanie(
        database=client[settings.database_name],
        document_models=[
            User, Course, Upload, Quiz, QuizQuestion, Chapter,
            QuizHistory, DashboardProgress, ChatSession, ChatMessage
        ]
    )


async def close_db():
    """Close database connection."""
    # Beanie handles connection cleanup automatically
    pass
