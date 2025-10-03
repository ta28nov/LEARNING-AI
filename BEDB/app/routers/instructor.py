"""Instructor-specific endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from bson import ObjectId

from app.schemas.enrollment import (
    StudentEnrollmentInfo,
    CourseAnalytics,
    InstructorDashboardResponse
)
from app.schemas.course import CourseResponse
from app.models.enrollment import CourseEnrollment, EnrollmentStatus, ChapterProgress
from app.models.course import Course
from app.models.user import User, UserRole
from app.auth import get_current_active_user

router = APIRouter(prefix="/instructor", tags=["instructor"])


async def get_instructor_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current user and verify instructor role."""
    if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Instructor or admin access required"
        )
    return current_user


@router.get("/courses", response_model=List[CourseResponse])
async def get_instructor_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    instructor: User = Depends(get_instructor_user)
):
    """Get all courses created by the instructor."""
    try:
        # Get courses owned by instructor
        courses = await Course.find(
            Course.owner_id == instructor.id
        ).skip(skip).limit(limit).to_list()
        
        return [CourseResponse.model_validate(course) for course in courses]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get instructor courses: {str(e)}"
        )


@router.get("/courses/{course_id}/students", response_model=List[StudentEnrollmentInfo])
async def get_course_students(
    course_id: str,
    status_filter: Optional[str] = Query(None, pattern="^(active|completed|dropped)$"),
    instructor: User = Depends(get_instructor_user)
):
    """Get all students enrolled in a specific course."""
    try:
        # Verify course ownership (unless admin)
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if instructor.role != UserRole.ADMIN and course.owner_id != instructor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view students for this course"
            )
        
        # Build query
        query = {CourseEnrollment.course_id: ObjectId(course_id)}
        if status_filter:
            query[CourseEnrollment.status] = status_filter
        
        # Get enrollments
        enrollments = await CourseEnrollment.find(query).to_list()
        
        # Get student details
        students_info = []
        for enrollment in enrollments:
            student = await User.get(enrollment.student_id)
            if student:
                students_info.append(
                    StudentEnrollmentInfo(
                        student_id=str(student.id),
                        student_name=student.name,
                        student_email=student.email,
                        enrolled_at=enrollment.enrolled_at,
                        progress=enrollment.progress,
                        status=enrollment.status,
                        last_accessed=enrollment.last_accessed
                    )
                )
        
        return students_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get course students: {str(e)}"
        )


@router.get("/courses/{course_id}/analytics", response_model=CourseAnalytics)
async def get_course_analytics(
    course_id: str,
    instructor: User = Depends(get_instructor_user)
):
    """Get detailed analytics for a specific course."""
    try:
        # Verify course ownership
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        if instructor.role != UserRole.ADMIN and course.owner_id != instructor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view analytics for this course"
            )
        
        # Get all enrollments
        all_enrollments = await CourseEnrollment.find(
            CourseEnrollment.course_id == ObjectId(course_id)
        ).to_list()
        
        total_enrollments = len(all_enrollments)
        active_students = len([e for e in all_enrollments if e.status == EnrollmentStatus.ACTIVE])
        completed_students = len([e for e in all_enrollments if e.status == EnrollmentStatus.COMPLETED])
        
        # Calculate average progress
        avg_progress = 0.0
        if all_enrollments:
            avg_progress = sum(e.progress for e in all_enrollments) / len(all_enrollments)
        
        # Calculate completion rate
        completion_rate = 0.0
        if total_enrollments > 0:
            completion_rate = (completed_students / total_enrollments) * 100
        
        # Calculate average time spent
        chapter_progress_list = await ChapterProgress.find(
            ChapterProgress.course_id == ObjectId(course_id)
        ).to_list()
        
        avg_time_spent = 0
        if chapter_progress_list:
            total_time = sum(cp.time_spent for cp in chapter_progress_list)
            unique_users = len(set(cp.user_id for cp in chapter_progress_list))
            if unique_users > 0:
                avg_time_spent = total_time // unique_users
        
        return CourseAnalytics(
            course_id=str(course.id),
            title=course.title,
            total_enrollments=total_enrollments,
            active_students=active_students,
            completed_students=completed_students,
            average_progress=round(avg_progress, 2),
            average_time_spent=avg_time_spent,
            completion_rate=round(completion_rate, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get course analytics: {str(e)}"
        )


@router.get("/dashboard", response_model=InstructorDashboardResponse)
async def get_instructor_dashboard(
    instructor: User = Depends(get_instructor_user)
):
    """Get instructor dashboard with overall statistics."""
    try:
        # Get all courses by instructor
        courses = await Course.find(Course.owner_id == instructor.id).to_list()
        total_courses = len(courses)
        
        # Get all enrollments for instructor's courses
        course_ids = [course.id for course in courses]
        all_enrollments = []
        
        if course_ids:
            all_enrollments = await CourseEnrollment.find(
                CourseEnrollment.course_id.in_(course_ids)
            ).to_list()
        
        total_enrollments = len(all_enrollments)
        unique_students = len(set(e.student_id for e in all_enrollments))
        
        # Calculate average course rating (placeholder - will implement later)
        avg_rating = 0.0
        
        # Get analytics for recent courses (top 5)
        recent_analytics = []
        for course in courses[:5]:
            # Get enrollments for this course
            course_enrollments = [e for e in all_enrollments if e.course_id == course.id]
            
            total_enrollments_course = len(course_enrollments)
            active = len([e for e in course_enrollments if e.status == EnrollmentStatus.ACTIVE])
            completed = len([e for e in course_enrollments if e.status == EnrollmentStatus.COMPLETED])
            
            avg_progress = 0.0
            if course_enrollments:
                avg_progress = sum(e.progress for e in course_enrollments) / len(course_enrollments)
            
            completion_rate = 0.0
            if total_enrollments_course > 0:
                completion_rate = (completed / total_enrollments_course) * 100
            
            # Get time spent for this course
            chapter_progress_list = await ChapterProgress.find(
                ChapterProgress.course_id == course.id
            ).to_list()
            
            avg_time_spent = 0
            if chapter_progress_list:
                total_time = sum(cp.time_spent for cp in chapter_progress_list)
                unique_users = len(set(cp.user_id for cp in chapter_progress_list))
                if unique_users > 0:
                    avg_time_spent = total_time // unique_users
            
            recent_analytics.append(
                CourseAnalytics(
                    course_id=str(course.id),
                    title=course.title,
                    total_enrollments=total_enrollments_course,
                    active_students=active,
                    completed_students=completed,
                    average_progress=round(avg_progress, 2),
                    average_time_spent=avg_time_spent,
                    completion_rate=round(completion_rate, 2)
                )
            )
        
        return InstructorDashboardResponse(
            total_courses=total_courses,
            total_students=unique_students,
            total_enrollments=total_enrollments,
            average_course_rating=avg_rating,
            recent_analytics=recent_analytics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get instructor dashboard: {str(e)}"
        )


@router.get("/students", response_model=List[StudentEnrollmentInfo])
async def get_all_instructor_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    instructor: User = Depends(get_instructor_user)
):
    """Get all students across all instructor's courses."""
    try:
        # Get all courses by instructor
        courses = await Course.find(Course.owner_id == instructor.id).to_list()
        course_ids = [course.id for course in courses]
        
        if not course_ids:
            return []
        
        # Get all enrollments
        enrollments = await CourseEnrollment.find(
            CourseEnrollment.course_id.in_(course_ids),
            CourseEnrollment.status == EnrollmentStatus.ACTIVE
        ).skip(skip).limit(limit).to_list()
        
        # Get unique students
        student_dict = {}
        for enrollment in enrollments:
            if enrollment.student_id not in student_dict:
                student = await User.get(enrollment.student_id)
                if student:
                    student_dict[enrollment.student_id] = StudentEnrollmentInfo(
                        student_id=str(student.id),
                        student_name=student.name,
                        student_email=student.email,
                        enrolled_at=enrollment.enrolled_at,
                        progress=enrollment.progress,
                        status=enrollment.status,
                        last_accessed=enrollment.last_accessed
                    )
        
        return list(student_dict.values())
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get instructor students: {str(e)}"
        )
