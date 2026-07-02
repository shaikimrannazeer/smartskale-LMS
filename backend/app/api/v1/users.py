"""Users API routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_current_admin
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfile,
    PaginationResponse,
)
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginationResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[UserRole] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db),
) -> PaginationResponse:
    """List users with pagination and filtering.

    Args:
        page: Page number
        limit: Records per page
        search: Search query
        role: Filter by role
        is_active: Filter by active status
        sort_by: Sort field
        sort_order: Sort order
        current_user: Current authenticated user
        db: Database session

    Returns:
        Paginated user response
    """
    service = UserService(db)
    return service.list_users(
        page=page,
        limit=limit,
        search=search,
        role=role,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order,
        current_user=current_user,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Get user by ID.

    Args:
        user_id: User ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        User response
    """
    service = UserService(db)
    return service.get_user(user_id, current_user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Create new user.

    Args:
        user_data: User creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created user response
    """
    service = UserService(db)
    return service.create_user(user_data, current_user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Update user.

    Args:
        user_id: User ID to update
        update_data: Update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user response
    """
    service = UserService(db)
    return service.update_user(user_id, update_data, current_user)


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> dict:
    """Delete user (soft delete).

    Args:
        user_id: User ID to delete
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    service = UserService(db)
    return service.delete_user(user_id, current_user)


@router.patch("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Activate user.

    Args:
        user_id: User ID to activate
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user response
    """
    service = UserService(db)
    return service.activate_user(user_id, current_user)


@router.patch("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserResponse:
    """Deactivate user.

    Args:
        user_id: User ID to deactivate
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user response
    """
    service = UserService(db)
    return service.deactivate_user(user_id, current_user)


@router.get("/profile/me", response_model=UserProfile)
async def get_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserProfile:
    """Get current user profile.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User profile response
    """
    service = UserService(db)
    return service.get_user_profile(current_user)


@router.put("/profile/me", response_model=UserProfile)
async def update_profile(
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> UserProfile:
    """Update current user profile.

    Args:
        update_data: Update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user profile response
    """
    service = UserService(db)
    return service.update_user_profile(update_data, current_user)
