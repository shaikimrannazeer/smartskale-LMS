"""User service with business logic."""

from typing import Optional, Tuple, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ValidationError,
    ConflictError,
    NotFoundError,
    ForbiddenError,
)
from app.core.logging import get_logger
from app.core.security import hash_password
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfile,
    UserListResponse,
    PaginationResponse,
)

logger = get_logger(__name__)


class UserService:
    """User management service."""

    def __init__(self, db: Session) -> None:
        """Initialize service.

        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)

    def create_user(
        self,
        user_data: UserCreate,
        current_user: User,
    ) -> UserResponse:
        """Create new user.

        Args:
            user_data: User creation data
            current_user: Current authenticated user

        Returns:
            Created user response

        Raises:
            ForbiddenError: If user is not admin
            ConflictError: If email already exists
        """
        # Authorization check
        if current_user.role != UserRole.ADMIN:
            logger.warning(f"Non-admin user attempted to create user: {current_user.user_id}")
            raise ForbiddenError("Only admin users can create users")

        # Check if user already exists
        existing_user = self.user_repo.find_by_email(user_data.email, include_deleted=True)
        if existing_user:
            logger.warning(f"User creation attempted with existing email: {user_data.email}")
            raise ConflictError(f"Email {user_data.email} already exists")

        # Hash password
        password_hash = hash_password(user_data.password)

        # Create user
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=password_hash,
            phone=user_data.phone,
            role=user_data.role,
            created_by=current_user.user_id,
        )

        try:
            created_user = self.user_repo.create(user)
            logger.info(f"User created by {current_user.email}: {created_user.email}")
            return UserResponse.model_validate(created_user)
        except IntegrityError:
            logger.error(f"Database integrity error during user creation: {user_data.email}")
            raise ConflictError("Failed to create user")

    def update_user(
        self,
        user_id: str,
        update_data: UserUpdate,
        current_user: User,
    ) -> UserResponse:
        """Update user.

        Args:
            user_id: User ID to update
            update_data: Update data
            current_user: Current authenticated user

        Returns:
            Updated user response

        Raises:
            NotFoundError: If user not found
            ForbiddenError: If not authorized
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            logger.warning(f"Update attempted on non-existent user: {user_id}")
            raise NotFoundError("User not found")

        # Authorization check - admin or own profile
        if current_user.role != UserRole.ADMIN and current_user.user_id != user_id:
            logger.warning(
                f"User {current_user.user_id} attempted to update user {user_id}"
            )
            raise ForbiddenError("You can only update your own profile")

        # Update fields
        if update_data.full_name:
            user.full_name = update_data.full_name
        if update_data.phone is not None:
            user.phone = update_data.phone
        if update_data.bio is not None:
            user.bio = update_data.bio
        if update_data.profile_image is not None:
            user.profile_image = update_data.profile_image

        user.updated_by = current_user.user_id
        user.updated_at = datetime.utcnow()

        updated_user = self.user_repo.update(user)
        logger.info(f"User updated by {current_user.email}: {user.email}")
        return UserResponse.model_validate(updated_user)

    def delete_user(
        self,
        user_id: str,
        current_user: User,
    ) -> dict:
        """Soft delete user.

        Args:
            user_id: User ID to delete
            current_user: Current authenticated user

        Returns:
            Success message

        Raises:
            NotFoundError: If user not found
            ForbiddenError: If not admin
        """
        # Authorization check
        if current_user.role != UserRole.ADMIN:
            logger.warning(f"Non-admin user {current_user.user_id} attempted to delete user")
            raise ForbiddenError("Only admin users can delete users")

        user = self.user_repo.find_by_id(user_id)
        if not user:
            logger.warning(f"Delete attempted on non-existent user: {user_id}")
            raise NotFoundError("User not found")

        # Cannot delete admin users
        if user.role == UserRole.ADMIN and user.user_id != current_user.user_id:
            raise ForbiddenError("Cannot delete other admin users")

        self.user_repo.soft_delete(user)
        logger.info(f"User soft-deleted by {current_user.email}: {user.email}")
        return {"message": "User deleted successfully"}

    def activate_user(
        self,
        user_id: str,
        current_user: User,
    ) -> UserResponse:
        """Activate user.

        Args:
            user_id: User ID to activate
            current_user: Current authenticated user

        Returns:
            Updated user response

        Raises:
            NotFoundError: If user not found
            ForbiddenError: If not admin
        """
        # Authorization check
        if current_user.role != UserRole.ADMIN:
            logger.warning(f"Non-admin user {current_user.user_id} attempted to activate user")
            raise ForbiddenError("Only admin users can activate users")

        user = self.user_repo.find_by_id(user_id)
        if not user:
            logger.warning(f"Activate attempted on non-existent user: {user_id}")
            raise NotFoundError("User not found")

        user = self.user_repo.activate_user(user)
        logger.info(f"User activated by {current_user.email}: {user.email}")
        return UserResponse.model_validate(user)

    def deactivate_user(
        self,
        user_id: str,
        current_user: User,
    ) -> UserResponse:
        """Deactivate user.

        Args:
            user_id: User ID to deactivate
            current_user: Current authenticated user

        Returns:
            Updated user response

        Raises:
            NotFoundError: If user not found
            ForbiddenError: If not admin
        """
        # Authorization check
        if current_user.role != UserRole.ADMIN:
            logger.warning(
                f"Non-admin user {current_user.user_id} attempted to deactivate user"
            )
            raise ForbiddenError("Only admin users can deactivate users")

        user = self.user_repo.find_by_id(user_id)
        if not user:
            logger.warning(f"Deactivate attempted on non-existent user: {user_id}")
            raise NotFoundError("User not found")

        # Cannot deactivate self
        if user.user_id == current_user.user_id:
            raise ValidationError("You cannot deactivate your own account")

        user = self.user_repo.deactivate_user(user)
        logger.info(f"User deactivated by {current_user.email}: {user.email}")
        return UserResponse.model_validate(user)

    def get_user(
        self,
        user_id: str,
        current_user: User,
    ) -> UserResponse:
        """Get user by ID.

        Args:
            user_id: User ID
            current_user: Current authenticated user

        Returns:
            User response

        Raises:
            NotFoundError: If user not found
            ForbiddenError: If not authorized
        """
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        # Authorization check - admin or own profile
        if current_user.role != UserRole.ADMIN and current_user.user_id != user_id:
            logger.warning(
                f"User {current_user.user_id} attempted to view user {user_id}"
            )
            raise ForbiddenError("You can only view your own profile")

        return UserResponse.model_validate(user)

    def list_users(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        current_user: Optional[User] = None,
    ) -> PaginationResponse:
        """List users with filtering and pagination.

        Args:
            page: Page number
            limit: Records per page
            search: Search query
            role: Filter by role
            is_active: Filter by active status
            sort_by: Sort field
            sort_order: Sort order
            current_user: Current authenticated user

        Returns:
            Paginated user response

        Raises:
            ForbiddenError: If not admin
        """
        # Authorization check
        if current_user and current_user.role != UserRole.ADMIN:
            logger.warning(f"Non-admin user {current_user.user_id} attempted to list users")
            raise ForbiddenError("Only admin users can list all users")

        skip = (page - 1) * limit

        if search:
            users, total = self.user_repo.search_users(
                search, skip, limit, sort_by, sort_order
            )
        elif role or is_active is not None:
            users, total = self.user_repo.filter_users(
                role, is_active, skip, limit, sort_by, sort_order
            )
        else:
            users, total = self.user_repo.list_users(
                skip, limit, sort_by, sort_order
            )

        total_pages = (total + limit - 1) // limit
        items = [UserListResponse.model_validate(user) for user in users]

        return PaginationResponse(
            total_records=total,
            total_pages=total_pages,
            current_page=page,
            page_size=limit,
            items=items,
        )

    def get_user_profile(
        self,
        current_user: User,
    ) -> UserProfile:
        """Get current user profile.

        Args:
            current_user: Current authenticated user

        Returns:
            User profile response
        """
        return UserProfile.model_validate(current_user)

    def update_user_profile(
        self,
        update_data: UserUpdate,
        current_user: User,
    ) -> UserProfile:
        """Update current user profile.

        Args:
            update_data: Update data
            current_user: Current authenticated user

        Returns:
            Updated user profile response
        """
        if update_data.full_name:
            current_user.full_name = update_data.full_name
        if update_data.phone is not None:
            current_user.phone = update_data.phone
        if update_data.bio is not None:
            current_user.bio = update_data.bio
        if update_data.profile_image is not None:
            current_user.profile_image = update_data.profile_image

        current_user.updated_at = datetime.utcnow()
        updated_user = self.user_repo.update(current_user)
        logger.info(f"User profile updated: {current_user.email}")
        return UserProfile.model_validate(updated_user)
