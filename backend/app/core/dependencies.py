"""Authentication dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session

from app.core.exceptions import (
    UnauthorizedError,
    ForbiddenError,
)
from app.core.logging import get_logger
from app.core.security import decode_token
from app.db.database import get_db
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> User:
    """Get currently authenticated user.

    Args:
        credentials: HTTP Bearer credentials
        db: Database session

    Returns:
        Current user

    Raises:
        UnauthorizedError: If token is invalid or expired
        HTTPException: If user not found or inactive
    """
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        logger.warning("Invalid or expired token attempted")
        raise UnauthorizedError("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        logger.warning("Token missing user ID")
        raise UnauthorizedError("Invalid token")

    user_repo = UserRepository(db)
    user = user_repo.find_by_id(user_id)

    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_active:
        logger.warning(f"Inactive user attempted login: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )

    return user


async def get_current_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current admin user.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if admin

    Raises:
        ForbiddenError: If user is not admin
    """
    if current_user.role != UserRole.ADMIN:
        logger.warning(f"Non-admin user attempted admin access: {current_user.user_id}")
        raise ForbiddenError("Only admin users can access this resource")
    return current_user


async def get_current_trainer(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current trainer user.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user if trainer or admin

    Raises:
        ForbiddenError: If user is not trainer or admin
    """
    if current_user.role not in (UserRole.TRAINER, UserRole.ADMIN):
        logger.warning(
            f"Non-trainer user attempted trainer access: {current_user.user_id}"
        )
        raise ForbiddenError("Only trainer users can access this resource")
    return current_user


async def get_current_student(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current student user.

    Args:
        current_user: Current authenticated user

    Returns:
        Current user (all authenticated users are students at minimum)
    """
    return current_user
