"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    CurrentUserResponse,
    TokenResponse,
    RefreshTokenRequest,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user response
    """
    service = AuthService(db)
    return service.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Login user.

    Args:
        login_data: User login credentials
        db: Database session

    Returns:
        Token response with access and refresh tokens
    """
    service = AuthService(db)
    return service.login(login_data)


@router.post("/refresh")
async def refresh(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> dict:
    """Refresh access token.

    Args:
        request: Refresh token request
        db: Database session

    Returns:
        New access token
    """
    service = AuthService(db)
    access_token = service.refresh_token(request.refresh_token)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout() -> dict:
    """Logout user.

    Returns:
        Success message
    """
    service = AuthService(db=None)
    return service.logout()


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user_info(
    current_user: Annotated[User, Depends(get_current_user)],
) -> CurrentUserResponse:
    """Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user response
    """
    return CurrentUserResponse.model_validate(current_user)
