"""User management endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserResponse
from app.models.user import User
from app.auth import get_current_active_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])


class UserUpdateRequest(BaseModel):
    """User update request schema."""
    name: Optional[str] = None
    avatar: Optional[str] = None


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user information."""
    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.avatar is not None:
        current_user.avatar = user_data.avatar
    
    await current_user.save()
    return UserResponse.model_validate(current_user)
