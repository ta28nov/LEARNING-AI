"""Admin endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.auth import UserResponse
from app.schemas.course import CourseCreate, CourseResponse
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.quiz import QuizHistory
from app.auth import get_current_active_user
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])


class AdminStats(BaseModel):
    """Admin statistics schema."""
    total_users: int
    total_courses: int
    total_quizzes: int
    active_users: int


class UserRoleUpdate(BaseModel):
    """User role update schema."""
    role: UserRole


async def get_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user and verify admin role."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    admin_user: User = Depends(get_admin_user)
):
    """Get list of all users (admin only)."""
    users = await User.find().skip(skip).limit(limit).to_list()
    return [UserResponse.model_validate(user) for user in users]


@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    role_data: UserRoleUpdate,
    admin_user: User = Depends(get_admin_user)
):
    """Update user role (admin only)."""
    try:
        user = await User.get(ObjectId(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.role = role_data.role
        await user.save()
        
        return {"message": f"User role updated to {role_data.role}"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.get("/stats", response_model=AdminStats)
async def get_admin_stats(admin_user: User = Depends(get_admin_user)):
    """Get system statistics (admin only)."""
    try:
        total_users = await User.find().count()
        active_users = await User.find(User.is_active == True).count()
        total_courses = await Course.find().count()
        total_quizzes = await QuizHistory.find().count()
        
        return AdminStats(
            total_users=total_users,
            total_courses=total_courses,
            total_quizzes=total_quizzes,
            active_users=active_users
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@router.post("/courses", response_model=CourseResponse)
async def create_sample_course(
    course_data: CourseCreate,
    admin_user: User = Depends(get_admin_user)
):
    """Create a sample course (admin only)."""
    course = Course(
        owner_id=admin_user.id,
        title=course_data.title,
        description=course_data.description,
        outline=course_data.outline,
        source=course_data.source or "Admin Created",
        level=course_data.level,
        tags=course_data.tags
    )
    
    await course.insert()
    return CourseResponse.model_validate(course)


@router.get("/courses", response_model=List[CourseResponse])
async def get_all_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    admin_user: User = Depends(get_admin_user)
):
    """Get all courses (admin only)."""
    courses = await Course.find().skip(skip).limit(limit).to_list()
    return [CourseResponse.model_validate(course) for course in courses]


@router.delete("/courses/{course_id}")
async def delete_course_admin(
    course_id: str,
    admin_user: User = Depends(get_admin_user)
):
    """Delete any course (admin only)."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        await course.delete()
        return {"message": "Course deleted successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.post("/courses/import", response_model=CourseResponse)
async def import_course(
    title: str,
    content: str,
    description: str = None,
    admin_user: User = Depends(get_admin_user)
):
    """Import course (admin only)."""
    try:
        # Create imported course
        course = Course(
            owner_id=admin_user.id,
            title=title,
            description=description or f"Imported course: {title}",
            outline=content,
            source="Imported",
            level="beginner",
            tags=["imported", "admin-imported"]
        )
        
        await course.insert()
        
        return CourseResponse.model_validate(course)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import course: {str(e)}"
        )
