"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from datetime import timedelta
from app.schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, RefreshTokenRequest,
    LogoutRequest, EmailVerificationRequest, ForgotPasswordRequest, ResetPasswordRequest
)
from app.models.user import User
from app.auth import (
    get_password_hash, verify_password, create_access_token, create_refresh_token,
    verify_refresh_token, get_current_active_user
)
from app.config import settings
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """Register a new user."""
    # Check if user already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        name=user_data.name
    )
    
    await user.insert()
    user_data = user.to_json()
    return UserResponse.model_validate(user_data)


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return access token."""
    # Find user by email
    user = await User.find_one(User.email == user_credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    user_data = current_user.to_json()
    return UserResponse.model_validate(user_data)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    name: str = None,
    avatar: str = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update current user information."""
    if name is not None:
        current_user.name = name
    if avatar is not None:
        current_user.avatar = avatar
    
    await current_user.save()
    user_data = current_user.to_json()
    return UserResponse.model_validate(user_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(request: RefreshTokenRequest):
    """Refresh access token using refresh token."""
    payload = verify_refresh_token(request.refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    try:
        user = await User.get(ObjectId(user_id))
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, refresh_token=request.refresh_token, token_type="bearer")


@router.post("/logout")
async def logout(request: LogoutRequest = None):
    """Logout user (invalidate tokens)."""
    # In a real application, you would maintain a blacklist of tokens
    # For now, we'll just return success
    return {"message": "Logged out successfully"}


@router.post("/verify-email")
async def verify_email(request: EmailVerificationRequest):
    """Verify email with OTP code."""
    # In a real application, you would verify the OTP code
    # For now, we'll just return success
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest):
    """Request password reset."""
    # In a real application, you would send a reset email
    # For now, we'll just return success
    return {"message": "Password reset email sent"}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """Reset password with token."""
    # In a real application, you would verify the reset token
    # For now, we'll just return success
    return {"message": "Password reset successfully"}


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    name: str = None,
    avatar: str = None,
    current_user: User = Depends(get_current_active_user)
):
    """Update user profile."""
    if name is not None:
        current_user.name = name
    if avatar is not None:
        current_user.avatar = avatar
    
    await current_user.save()
    return UserResponse.model_validate(current_user)


@router.patch("/me/password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user)
):
    """Change user password."""
    # Verify current password
    if not verify_password(old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.password_hash = get_password_hash(new_password)
    await current_user.save()
    
    return {"message": "Password updated successfully"}
