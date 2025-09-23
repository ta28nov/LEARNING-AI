"""Dashboard endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.dashboard import DashboardStats, ProgressUpdate, CourseProgress
from app.models.dashboard import DashboardProgress, ProgressStatus
from app.models.course import Course, Chapter
from app.models.quiz import QuizHistory
from app.models.user import User
from app.auth import get_current_active_user
from bson import ObjectId
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=dict)
async def get_dashboard_overview(
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard overview statistics."""
    try:
        # Get user's courses
        user_courses = await Course.find(Course.owner_id == current_user.id).to_list()
        total_courses = len(user_courses)
        
        # Get completed courses
        completed_progress = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.status == ProgressStatus.COMPLETED
        ).to_list()
        completed_courses = len(set(p.course_id for p in completed_progress))
        
        # Get quiz statistics
        quiz_history = await QuizHistory.find(
            QuizHistory.user_id == current_user.id
        ).to_list()
        total_quizzes = len(quiz_history)
        
        # Calculate total time spent (in hours)
        total_time_spent = sum(p.time_spent for p in completed_progress) / 60  # Convert to hours
        
        # Calculate completion rate
        completion_rate = (completed_courses / total_courses * 100) if total_courses > 0 else 0
        
        return {
            "total_hours": round(total_time_spent, 1),
            "total_quizzes": total_quizzes,
            "completion_rate": round(completion_rate, 1)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard overview: {str(e)}"
        )


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics for the current user."""
    try:
        # Get user's courses
        user_courses = await Course.find(Course.owner_id == current_user.id).to_list()
        total_courses = len(user_courses)
        
        # Get completed courses
        completed_progress = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.status == ProgressStatus.COMPLETED
        ).to_list()
        completed_courses = len(set(p.course_id for p in completed_progress))
        
        # Get quiz statistics
        quiz_history = await QuizHistory.find(
            QuizHistory.user_id == current_user.id
        ).to_list()
        total_quizzes = len(quiz_history)
        
        # Calculate average score
        average_score = 0
        if quiz_history:
            total_score = sum(qh.score for qh in quiz_history)
            average_score = total_score / len(quiz_history)
        
        # Calculate total time spent
        total_time_spent = sum(p.time_spent for p in completed_progress)
        
        # Get recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_quiz_history = await QuizHistory.find(
            QuizHistory.user_id == current_user.id,
            QuizHistory.taken_at >= week_ago
        ).sort("-taken_at").limit(10).to_list()
        
        recent_activity = []
        for qh in recent_quiz_history:
            recent_activity.append({
                "type": "quiz",
                "title": f"Quiz completed",
                "score": qh.score,
                "date": qh.taken_at
            })
        
        # Get progress by course
        progress_by_course = []
        for course in user_courses:
            course_progress = await DashboardProgress.find(
                DashboardProgress.user_id == current_user.id,
                DashboardProgress.course_id == course.id
            ).to_list()
            
            if course_progress:
                avg_progress = sum(p.progress for p in course_progress) / len(course_progress)
                progress_by_course.append({
                    "course_id": str(course.id),
                    "course_title": course.title,
                    "progress": avg_progress
                })
        
        # Get weekly progress (last 4 weeks)
        weekly_progress = []
        for i in range(4):
            week_start = datetime.utcnow() - timedelta(weeks=i+1)
            week_end = datetime.utcnow() - timedelta(weeks=i)
            
            week_quiz_history = await QuizHistory.find(
                QuizHistory.user_id == current_user.id,
                QuizHistory.taken_at >= week_start,
                QuizHistory.taken_at < week_end
            ).to_list()
            
            weekly_progress.append({
                "week": f"Week {4-i}",
                "quizzes_taken": len(week_quiz_history),
                "average_score": sum(qh.score for qh in week_quiz_history) / len(week_quiz_history) if week_quiz_history else 0
            })
        
        return DashboardStats(
            total_courses=total_courses,
            completed_courses=completed_courses,
            total_quizzes=total_quizzes,
            total_time_spent=total_time_spent,
            average_score=average_score,
            recent_activity=recent_activity,
            progress_by_course=progress_by_course,
            weekly_progress=weekly_progress
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard stats: {str(e)}"
        )


@router.get("/progress", response_model=List[CourseProgress])
async def get_course_progress(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get course progress for the current user."""
    try:
        # Get user's progress records
        progress_records = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id
        ).skip(skip).limit(limit).sort("-last_accessed").to_list()
        
        course_progress = []
        for progress in progress_records:
            # Get course details
            course = await Course.get(progress.course_id)
            if not course:
                continue
            
            # Get chapter count
            total_chapters = await Chapter.find(Chapter.course_id == course.id).count()
            
            # Get completed chapters
            completed_chapters = await DashboardProgress.find(
                DashboardProgress.user_id == current_user.id,
                DashboardProgress.course_id == course.id,
                DashboardProgress.status == ProgressStatus.COMPLETED
            ).count()
            
            course_progress.append(CourseProgress(
                course_id=str(course.id),
                course_title=course.title,
                progress=progress.progress,
                status=progress.status,
                time_spent=progress.time_spent,
                last_accessed=progress.last_accessed,
                chapters_completed=completed_chapters,
                total_chapters=total_chapters
            ))
        
        return course_progress
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get course progress: {str(e)}"
        )


@router.post("/progress", response_model=dict)
async def update_progress(
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update user's progress for a course or chapter."""
    try:
        # Verify course exists
        course = await Course.get(ObjectId(progress_data.course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Verify chapter exists if provided
        if progress_data.chapter_id:
            chapter = await Chapter.get(ObjectId(progress_data.chapter_id))
            if not chapter or str(chapter.course_id) != progress_data.course_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chapter not found"
                )
        
        # Find existing progress record
        existing_progress = await DashboardProgress.find_one(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.course_id == ObjectId(progress_data.course_id),
            DashboardProgress.chapter_id == ObjectId(progress_data.chapter_id) if progress_data.chapter_id else None
        )
        
        if existing_progress:
            # Update existing progress
            existing_progress.status = progress_data.status
            existing_progress.progress = progress_data.progress
            existing_progress.time_spent += progress_data.time_spent
            existing_progress.last_accessed = datetime.utcnow()
            await existing_progress.save()
        else:
            # Create new progress record
            new_progress = DashboardProgress(
                user_id=current_user.id,
                course_id=ObjectId(progress_data.course_id),
                chapter_id=ObjectId(progress_data.chapter_id) if progress_data.chapter_id else None,
                status=progress_data.status,
                progress=progress_data.progress,
                time_spent=progress_data.time_spent
            )
            await new_progress.insert()
        
        return {"message": "Progress updated successfully"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course or chapter not found"
        )


@router.get("/progress/{course_id}", response_model=List[dict])
async def get_course_progress_detail(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed progress for a specific course."""
    try:
        # Verify course exists
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Get course progress
        course_progress = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.course_id == course.id
        ).to_list()
        
        # Get chapters
        chapters = await Chapter.find(Chapter.course_id == course.id).sort("order").to_list()
        
        progress_detail = []
        for chapter in chapters:
            chapter_progress = next(
                (p for p in course_progress if p.chapter_id == chapter.id), 
                None
            )
            
            progress_detail.append({
                "chapter_id": str(chapter.id),
                "chapter_title": chapter.title,
                "chapter_order": chapter.order,
                "status": chapter_progress.status if chapter_progress else ProgressStatus.NOT_STARTED,
                "progress": chapter_progress.progress if chapter_progress else 0.0,
                "time_spent": chapter_progress.time_spent if chapter_progress else 0,
                "last_accessed": chapter_progress.last_accessed if chapter_progress else None
            })
        
        return progress_detail
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )


@router.get("/recommendations", response_model=List[dict])
async def get_learning_recommendations(
    current_user: User = Depends(get_current_active_user)
):
    """Get personalized learning recommendations."""
    try:
        recommendations = []
        
        # Get user's progress
        progress_records = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id
        ).to_list()
        
        # Find courses that need attention
        for progress in progress_records:
            if progress.status == ProgressStatus.IN_PROGRESS and progress.progress < 50:
                course = await Course.get(progress.course_id)
                if course:
                    recommendations.append({
                        "type": "continue_course",
                        "title": f"Continue learning: {course.title}",
                        "description": f"You're {progress.progress:.1f}% through this course",
                        "course_id": str(course.id),
                        "priority": "high"
                    })
        
        # Find courses that haven't been started recently
        recent_progress = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.last_accessed >= datetime.utcnow() - timedelta(days=7)
        ).to_list()
        
        all_courses = await Course.find(Course.owner_id == current_user.id).to_list()
        for course in all_courses:
            has_recent_progress = any(p.course_id == course.id for p in recent_progress)
            if not has_recent_progress:
                recommendations.append({
                    "type": "review_course",
                    "title": f"Review: {course.title}",
                    "description": "You haven't accessed this course recently",
                    "course_id": str(course.id),
                    "priority": "medium"
                })
        
        # Get quiz performance recommendations
        recent_quizzes = await QuizHistory.find(
            QuizHistory.user_id == current_user.id,
            QuizHistory.taken_at >= datetime.utcnow() - timedelta(days=30)
        ).sort("-taken_at").limit(10).to_list()
        
        low_score_quizzes = [q for q in recent_quizzes if q.score < 70]
        if low_score_quizzes:
            recommendations.append({
                "type": "review_quizzes",
                "title": "Review recent quiz performance",
                "description": f"You scored below 70% on {len(low_score_quizzes)} recent quizzes",
                "priority": "high"
            })
        
        return recommendations[:5]  # Return top 5 recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )


@router.get("/course-stats/{course_id}")
async def get_course_stats(
    course_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get statistics for a specific course."""
    try:
        course = await Course.get(ObjectId(course_id))
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        # Get user's progress for this course
        progress = await DashboardProgress.find(
            DashboardProgress.user_id == current_user.id,
            DashboardProgress.course_id == course.id
        ).to_list()
        
        # Get quiz history for this course
        quiz_history = await QuizHistory.find(
            QuizHistory.user_id == current_user.id
        ).to_list()
        
        # Filter quiz history for this course
        course_quizzes = []
        for qh in quiz_history:
            quiz = await Quiz.get(qh.quiz_id)
            if quiz and quiz.course_id == course.id:
                course_quizzes.append(qh)
        
        # Calculate statistics
        total_time_spent = sum(p.time_spent for p in progress)
        average_score = sum(q.score for q in course_quizzes) / len(course_quizzes) if course_quizzes else 0
        completion_rate = sum(1 for p in progress if p.status == ProgressStatus.COMPLETED) / len(progress) * 100 if progress else 0
        
        return {
            "course_id": str(course.id),
            "course_title": course.title,
            "total_time_spent": total_time_spent,
            "average_score": round(average_score, 1),
            "completion_rate": round(completion_rate, 1),
            "quizzes_taken": len(course_quizzes),
            "chapters_completed": len([p for p in progress if p.status == ProgressStatus.COMPLETED])
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
