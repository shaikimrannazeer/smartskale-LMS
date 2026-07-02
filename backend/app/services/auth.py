"""Authentication service with business logic."""

from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ValidationError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
)
from app.core.logging import get_logger
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    CurrentUserResponse,
    TokenResponse,
)

logger = get_logger(__name__)


class AuthService:
    """Authentication service."""

    def __init__(self, db: Session) -> None:
        """Initialize service.

        Args:
            db: Database session
        """
        self.db = db
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> UserResponse:
        """Register new user.

        Args:
            user_data: User registration data

        Returns:
            Created user response

        Raises:
            ConflictError: If email already exists
            ValidationError: If validation fails
        """
        # Check if user already exists
        existing_user = self.user_repo.find_by_email(user_data.email)
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {user_data.email}")
            raise ConflictError(f"Email {user_data.email} already registered")

        # Hash password
        password_hash = hash_password(user_data.password)

        # Create user
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=password_hash,
            role=user_data.role,
        )

        try:
            created_user = self.user_repo.create(user)
            logger.info(f"User registered: {created_user.email}")
            return UserResponse.model_validate(created_user)
        except IntegrityError:
            logger.error(f"Database integrity error during registration: {user_data.email}")
            raise ConflictError("Failed to register user")

    def login(self, login_data: UserLogin) -> TokenResponse:
        """Login user.

        Args:
            login_data: User login credentials

        Returns:
            Token response with access and refresh tokens

        Raises:
            UnauthorizedError: If credentials are invalid
            ValidationError: If user is inactive
        """
        # Find user by email
        user = self.user_repo.find_by_email(login_data.email)
        if not user:
            logger.warning(f"Login attempt with non-existent email: {login_data.email}")
            raise UnauthorizedError("Invalid email or password")

        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt by inactive user: {user.email}")
            raise ValidationError("User account is inactive")

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            logger.warning(f"Failed login attempt for: {user.email}")
            raise UnauthorizedError("Invalid email or password")

        # Update last login
        self.user_repo.update_last_login(user)

        # Create tokens
        access_token = create_access_token(
            data={"sub": user.user_id},
            expires_delta=timedelta(minutes=15),
        )
        refresh_token = create_refresh_token(data={"sub": user.user_id})

        logger.info(f"User logged in: {user.email}")

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=CurrentUserResponse.model_validate(user),
        )

    def refresh_token(self, refresh_token: str) -> str:
        """Refresh access token.

        Args:
            refresh_token: Refresh token

        Returns:
            New access token

        Raises:
            UnauthorizedError: If refresh token is invalid
        """
        payload = decode_token(refresh_token)
        if not payload:
            logger.warning("Invalid refresh token attempted")
            raise UnauthorizedError("Invalid refresh token")

        token_type = payload.get("type")
        if token_type != "refresh":
            logger.warning("Non-refresh token used for refresh")
            raise UnauthorizedError("Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            logger.warning("Refresh token missing user ID")
            raise UnauthorizedError("Invalid token")

        # Create new access token
        access_token = create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(minutes=15),
        )

        logger.info(f"Token refreshed for user: {user_id}")
        return access_token

    def logout(self) -> dict:
        """Logout user.

        Returns:
            Success message
        """
        logger.info("User logged out")
        return {"message": "Successfully logged out"}

    def get_current_user(self, user: User) -> CurrentUserResponse:
        """Get current user data.

        Args:
            user: User model instance

        Returns:
            Current user response
        """
        return CurrentUserResponse.model_validate(user)
