"""
Pytest configuration and fixtures for testing
"""
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import CourseEnrollment, ChapterProgress
from app.auth import create_access_token
import hashlib

# Test database name
TEST_DATABASE_NAME = "ai_learning_platform_test"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator:
    """
    Create a test database connection and initialize Beanie.
    Clean up after each test.
    """
    # Connect to test database
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[TEST_DATABASE_NAME]
    
    # Initialize Beanie with test models
    await init_beanie(
        database=db,
        document_models=[
            User,
            Course,
            CourseEnrollment,
            ChapterProgress
        ]
    )
    
    yield db
    
    # Clean up: Drop all collections after test
    for collection_name in await db.list_collection_names():
        await db[collection_name].drop()
    
    client.close()


@pytest.fixture
async def test_student(test_db) -> User:
    """Create a test student user."""
    password_hash = hashlib.sha256("student123".encode()).hexdigest()
    user = User(
        email="student@test.com",
        password_hash=password_hash,
        name="Test Student",
        role="student",
        is_active=True
    )
    await user.insert()
    return user


@pytest.fixture
async def test_instructor(test_db) -> User:
    """Create a test instructor user."""
    password_hash = hashlib.sha256("instructor123".encode()).hexdigest()
    user = User(
        email="instructor@test.com",
        password_hash=password_hash,
        name="Test Instructor",
        role="instructor",
        is_active=True
    )
    await user.insert()
    return user


@pytest.fixture
async def test_admin(test_db) -> User:
    """Create a test admin user."""
    password_hash = hashlib.sha256("admin123".encode()).hexdigest()
    user = User(
        email="admin@test.com",
        password_hash=password_hash,
        name="Test Admin",
        role="admin",
        is_active=True
    )
    await user.insert()
    return user


@pytest.fixture
async def test_course(test_db, test_instructor) -> Course:
    """Create a test course."""
    course = Course(
        title="Test Course",
        description="A test course for testing",
        outline="Chapter 1\nChapter 2\nChapter 3",
        level="beginner",
        tags=["test", "python"],
        owner_id=test_instructor.id,
        source="manual",
        is_public=True,
        visibility="public",
        is_approved=True,
        enrollment_count=0
    )
    await course.insert()
    return course


@pytest.fixture
async def test_draft_course(test_db, test_instructor) -> Course:
    """Create a test draft course."""
    course = Course(
        title="Draft Test Course",
        description="A draft course for testing",
        outline="Chapter 1",
        level="intermediate",
        tags=["test", "draft"],
        owner_id=test_instructor.id,
        source="manual",
        is_public=False,
        visibility="draft",
        is_approved=False,
        enrollment_count=0
    )
    await course.insert()
    return course


@pytest.fixture
async def test_enrollment(test_db, test_student, test_course) -> CourseEnrollment:
    """Create a test enrollment."""
    enrollment = CourseEnrollment(
        student_id=test_student.id,
        course_id=test_course.id,
        status="active",
        progress=25.0
    )
    await enrollment.insert()
    
    # Update course enrollment count
    test_course.enrollment_count += 1
    await test_course.save()
    
    return enrollment


@pytest.fixture
def student_token(test_student) -> str:
    """Generate JWT token for test student."""
    return create_access_token({"sub": str(test_student.id), "role": "student"})


@pytest.fixture
def instructor_token(test_instructor) -> str:
    """Generate JWT token for test instructor."""
    return create_access_token({"sub": str(test_instructor.id), "role": "instructor"})


@pytest.fixture
def admin_token(test_admin) -> str:
    """Generate JWT token for test admin."""
    return create_access_token({"sub": str(test_admin.id), "role": "admin"})
