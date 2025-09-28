#!/usr/bin/env python3
"""
Test script to verify backend setup and MongoDB connection.
Run this script to check if everything is working correctly.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.database import init_db
from app.config import settings
from app.models import User, Course, Chapter, Upload, Quiz, QuizQuestion, QuizHistory, ChatSession, ChatMessage, DashboardProgress

async def test_database_connection():
    """Test database connection and model initialization."""
    print("🔍 Testing database connection...")
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database connection successful!")
        
        # Test model creation (without saving)
        print("🔍 Testing model creation...")
        
        # Test User model
        test_user = User(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User"
        )
        print("✅ User model created successfully")
        
        # Test Course model
        test_course = Course(
            owner_id=test_user.id,
            title="Test Course",
            description="A test course description",
            level="beginner"
        )
        print("✅ Course model created successfully")
        
        # Test Chapter model
        test_chapter = Chapter(
            course_id=test_course.id,
            title="Test Chapter",
            content="Test chapter content",
            order=1
        )
        print("✅ Chapter model created successfully")
        
        # Test ObjectId to string conversion
        print("🔍 Testing ObjectId conversion...")
        user_id_str = str(test_user.id)
        course_id_str = str(test_course.id)
        print(f"✅ User ID as string: {user_id_str}")
        print(f"✅ Course ID as string: {course_id_str}")
        
        # Test Upload model
        test_upload = Upload(
            user_id=test_user.id,
            filename="test.pdf",
            file_type="pdf",
            file_path="/uploads/test.pdf",
            file_size=1024
        )
        print("✅ Upload model created successfully")
        
        # Test Quiz model
        test_quiz = Quiz(
            course_id=test_course.id,
            title="Test Quiz",
            prompt="Test quiz prompt"
        )
        print("✅ Quiz model created successfully")
        
        # Test QuizQuestion model
        test_question = QuizQuestion(
            quiz_id=test_quiz.id,
            question="What is the test question?",
            options=["Option 1", "Option 2", "Option 3", "Option 4"],
            correct_answer=0,
            order=1
        )
        print("✅ QuizQuestion model created successfully")
        
        # Test QuizHistory model
        test_history = QuizHistory(
            quiz_id=test_quiz.id,
            user_id=test_user.id,
            score=85.5,
            answers=[0, 1, 2, 3]
        )
        print("✅ QuizHistory model created successfully")
        
        # Test ChatSession model
        test_chat_session = ChatSession(
            user_id=test_user.id,
            title="Test Chat Session",
            mode="hybrid"
        )
        print("✅ ChatSession model created successfully")
        
        # Test ChatMessage model
        test_message = ChatMessage(
            session_id=test_chat_session.id,
            sender="user",
            message="Hello, this is a test message"
        )
        print("✅ ChatMessage model created successfully")
        
        # Test DashboardProgress model
        test_progress = DashboardProgress(
            user_id=test_user.id,
            course_id=test_course.id,
            progress=25.0,
            status="in_progress"
        )
        print("✅ DashboardProgress model created successfully")
        
        print("\n🎉 All models are working correctly!")
        print(f"📊 Database: {settings.database_name}")
        print(f"🔗 MongoDB URL: {settings.mongodb_url}")
        print(f"🌐 Server will run on: {settings.host}:{settings.port}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Starting backend setup verification...")
    print("=" * 50)
    
    success = await test_database_connection()
    
    print("=" * 50)
    if success:
        print("✅ Backend setup verification completed successfully!")
        print("🚀 You can now start the server with: python -m uvicorn app.main:app --reload")
    else:
        print("❌ Backend setup verification failed!")
        print("🔧 Please check the error messages above and fix the issues.")
    
    return success

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)
