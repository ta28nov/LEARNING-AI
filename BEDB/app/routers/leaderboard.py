"""Leaderboard endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from app.models.user import User
from app.models.quiz import QuizHistory
from app.models.dashboard import DashboardProgress, ProgressStatus
from app.auth import get_current_active_user
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


class LeaderboardEntry(BaseModel):
    """Leaderboard entry schema."""
    user_id: str
    user_name: str
    score: float
    quizzes_taken: int
    courses_completed: int


@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get leaderboard rankings."""
    try:
        # Get all users with their quiz performance
        users = await User.find(User.is_active == True).to_list()
        leaderboard = []
        
        for user in users:
            # Get user's quiz history
            quiz_history = await QuizHistory.find(
                QuizHistory.user_id == user.id
            ).to_list()
            
            # Get user's completed courses
            completed_progress = await DashboardProgress.find(
                DashboardProgress.user_id == user.id,
                DashboardProgress.status == ProgressStatus.COMPLETED
            ).to_list()
            
            if quiz_history:  # Only include users who have taken quizzes
                average_score = sum(qh.score for qh in quiz_history) / len(quiz_history)
                leaderboard.append(LeaderboardEntry(
                    user_id=str(user.id),
                    user_name=user.name,
                    score=round(average_score, 1),
                    quizzes_taken=len(quiz_history),
                    courses_completed=len(set(p.course_id for p in completed_progress))
                ))
        
        # Sort by average score (descending)
        leaderboard.sort(key=lambda x: x.score, reverse=True)
        
        return leaderboard[:limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get leaderboard: {str(e)}"
        )
