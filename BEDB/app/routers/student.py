"""Course enrollment endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.schemas.enrollment import (
    CourseEnrollmentResponse,
    EnrolledCourseInfo,
    StudentDashboardResponse
)
from app.models.enrollment import CourseEnrollment, EnrollmentStatus
from app.models.course import Course, CourseVisibility
from app.models.user import User, UserRole
from app.auth import get_current_active_user

router = APIRouter(prefix="/student", tags=["student"])


@router.post("/courses/{course_id}/enroll", response_model=CourseEnrollmentResponse)
async def enroll_in_course(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Enroll in a course (student only)."""
    # Only students can enroll
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses"
        )
    
    try:
        # Check if course exists
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Check if course is accessible (public or approved)
        if course.visibility == CourseVisibility.DRAFT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot enroll in draft courses"
            )
        
        if course.visibility == CourseVisibility.PRIVATE and not course.is_approved:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot enroll in private courses"
            )
        
        # Check if already enrolled
        existing_enrollment = await CourseEnrollment.find_one(
            CourseEnrollment.student_id == current_user.id,
            CourseEnrollment.course_id == ObjectId(course_id)
        )
        
        if existing_enrollment:
            # If previously dropped, reactivate
            if existing_enrollment.status == EnrollmentStatus.DROPPED:
                existing_enrollment.status = EnrollmentStatus.ACTIVE
                existing_enrollment.enrolled_at = datetime.utcnow()
                await existing_enrollment.save()
                
                # Update enrollment count
                course.enrollment_count += 1
                await course.save()
                
                return CourseEnrollmentResponse.model_validate(existing_enrollment)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already enrolled in this course"
                )
        
        # Create new enrollment
        enrollment = CourseEnrollment(
            student_id=current_user.id,
            course_id=ObjectId(course_id),
            enrolled_at=datetime.utcnow(),
            status=EnrollmentStatus.ACTIVE,
            progress=0.0
        )
        
        await enrollment.insert()
        
        # Update course enrollment count
        course.enrollment_count += 1
        await course.save()
        
        return CourseEnrollmentResponse.model_validate(enrollment)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enroll in course: {str(e)}"
        )


@router.delete("/courses/{course_id}/enroll")
async def unenroll_from_course(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Unenroll from a course (student only)."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can unenroll from courses"
        )
    
    try:
        # Find enrollment
        enrollment = await CourseEnrollment.find_one(
            CourseEnrollment.student_id == current_user.id,
            CourseEnrollment.course_id == ObjectId(course_id),
            CourseEnrollment.status == EnrollmentStatus.ACTIVE
        )
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found or already dropped"
            )
        
        # Update enrollment status
        enrollment.status = EnrollmentStatus.DROPPED
        await enrollment.save()
        
        # Update course enrollment count
        course = await Course.get(ObjectId(course_id))
        if course and course.enrollment_count > 0:
            course.enrollment_count -= 1
            await course.save()
        
        return {"message": "Successfully unenrolled from course"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unenroll from course: {str(e)}"
        )


@router.get("/enrolled-courses", response_model=List[EnrolledCourseInfo])
async def get_enrolled_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None, pattern="^(active|completed|dropped)$"),
    current_user: User = Depends(get_current_active_user)
):
    """Get all courses enrolled by the current student."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access enrolled courses"
        )
    
    try:
        # Build query
        query = {CourseEnrollment.student_id: current_user.id}
        if status:
            query[CourseEnrollment.status] = status
        
        # Get enrollments
        enrollments = await CourseEnrollment.find(
            query
        ).skip(skip).limit(limit).to_list()
        
        # Get course details for each enrollment
        enrolled_courses = []
        for enrollment in enrollments:
            course = await Course.get(enrollment.course_id)
            if course:
                enrolled_courses.append(
                    EnrolledCourseInfo(
                        course_id=str(course.id),
                        title=course.title,
                        description=course.description,
                        level=course.level,
                        enrollment_status=enrollment.status,
                        progress=enrollment.progress,
                        enrolled_at=enrollment.enrolled_at,
                        last_accessed=enrollment.last_accessed
                    )
                )
        
        return enrolled_courses
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get enrolled courses: {str(e)}"
        )


@router.get("/dashboard", response_model=StudentDashboardResponse)
async def get_student_dashboard(
    current_user: User = Depends(get_current_active_user)
):
    """Get student dashboard with statistics."""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access student dashboard"
        )
    
    try:
        # Get all enrollments
        all_enrollments = await CourseEnrollment.find(
            CourseEnrollment.student_id == current_user.id
        ).to_list()
        
        total_enrolled = len([e for e in all_enrollments if e.status == EnrollmentStatus.ACTIVE])
        completed = len([e for e in all_enrollments if e.status == EnrollmentStatus.COMPLETED])
        in_progress = total_enrolled - completed
        
        # Calculate average progress and total time spent
        avg_progress = 0.0
        total_time = 0
        
        if all_enrollments:
            avg_progress = sum(e.progress for e in all_enrollments) / len(all_enrollments)
            
            # Get chapter progress for time calculation
            from app.models.enrollment import ChapterProgress
            all_chapter_progress = await ChapterProgress.find(
                ChapterProgress.user_id == current_user.id
            ).to_list()
            total_time = sum(cp.time_spent for cp in all_chapter_progress)
        
        # Get recent courses (last 5)
        recent_enrollments = await CourseEnrollment.find(
            CourseEnrollment.student_id == current_user.id,
            CourseEnrollment.status == EnrollmentStatus.ACTIVE
        ).sort(-CourseEnrollment.enrolled_at).limit(5).to_list()
        
        recent_courses = []
        for enrollment in recent_enrollments:
            course = await Course.get(enrollment.course_id)
            if course:
                recent_courses.append(
                    EnrolledCourseInfo(
                        course_id=str(course.id),
                        title=course.title,
                        description=course.description,
                        level=course.level,
                        enrollment_status=enrollment.status,
                        progress=enrollment.progress,
                        enrolled_at=enrollment.enrolled_at,
                        last_accessed=enrollment.last_accessed
                    )
                )
        
        return StudentDashboardResponse(
            total_enrolled_courses=total_enrolled,
            completed_courses=completed,
            in_progress_courses=in_progress,
            total_time_spent=total_time,
            average_progress=round(avg_progress, 2),
            recent_courses=recent_courses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get student dashboard: {str(e)}"
        )
