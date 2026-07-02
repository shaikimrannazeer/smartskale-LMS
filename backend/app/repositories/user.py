"""User repository for data access."""

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    """User data access repository."""

    def __init__(self, db: Session) -> None:
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    def create(self, user: User) -> User:
        """Create new user.

        Args:
            user: User model instance

        Returns:
            Created user
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID.

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.user_id == user_id)
        return self.db.scalar(stmt)

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email.

        Args:
            email: User email

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def update_last_login(self, user: User) -> User:
        """Update user's last login timestamp.

        Args:
            user: User model instance

        Returns:
            Updated user
        """
        user.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user
