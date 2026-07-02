"""User repository for data access."""

from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, desc, asc

from app.models.user import User, UserRole


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

    def update(self, user: User) -> User:
        """Update user.

        Args:
            user: User model instance

        Returns:
            Updated user
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Permanently delete user.

        Args:
            user: User model instance
        """
        self.db.delete(user)
        self.db.commit()

    def soft_delete(self, user: User) -> User:
        """Soft delete user (mark as deleted).

        Args:
            user: User model instance

        Returns:
            Updated user
        """
        user.is_deleted = True
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_id(self, user_id: str, include_deleted: bool = False) -> Optional[User]:
        """Find user by ID.

        Args:
            user_id: User ID
            include_deleted: Include deleted users

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.user_id == user_id)
        if not include_deleted:
            stmt = stmt.where(User.is_deleted == False)
        return self.db.scalar(stmt)

    def find_by_email(self, email: str, include_deleted: bool = False) -> Optional[User]:
        """Find user by email.

        Args:
            email: User email
            include_deleted: Include deleted users

        Returns:
            User if found, None otherwise
        """
        stmt = select(User).where(User.email == email)
        if not include_deleted:
            stmt = stmt.where(User.is_deleted == False)
        return self.db.scalar(stmt)

    def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[List[User], int]:
        """List users with pagination and sorting.

        Args:
            skip: Number of records to skip
            limit: Number of records to return
            sort_by: Field to sort by
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (users list, total count)
        """
        stmt = select(User).where(User.is_deleted == False)

        # Sort
        sort_field = getattr(User, sort_by, User.created_at)
        if sort_order.lower() == "asc":
            stmt = stmt.order_by(asc(sort_field))
        else:
            stmt = stmt.order_by(desc(sort_field))

        # Count total
        count_stmt = select(User).where(User.is_deleted == False)
        total = len(self.db.scalars(count_stmt).all())

        # Paginate
        stmt = stmt.offset(skip).limit(limit)
        users = self.db.scalars(stmt).all()

        return users, total

    def search_users(
        self,
        query: str,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[List[User], int]:
        """Search users by name, email, or phone.

        Args:
            query: Search query
            skip: Number of records to skip
            limit: Number of records to return
            sort_by: Field to sort by
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (users list, total count)
        """
        search_term = f"%{query}%"
        stmt = select(User).where(
            and_(
                User.is_deleted == False,
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone.ilike(search_term),
                ),
            )
        )

        # Sort
        sort_field = getattr(User, sort_by, User.created_at)
        if sort_order.lower() == "asc":
            stmt = stmt.order_by(asc(sort_field))
        else:
            stmt = stmt.order_by(desc(sort_field))

        # Count total
        count_stmt = select(User).where(
            and_(
                User.is_deleted == False,
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.phone.ilike(search_term),
                ),
            )
        )
        total = len(self.db.scalars(count_stmt).all())

        # Paginate
        stmt = stmt.offset(skip).limit(limit)
        users = self.db.scalars(stmt).all()

        return users, total

    def filter_users(
        self,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[List[User], int]:
        """Filter users by role and active status.

        Args:
            role: Filter by role
            is_active: Filter by active status
            skip: Number of records to skip
            limit: Number of records to return
            sort_by: Field to sort by
            sort_order: Sort order (asc or desc)

        Returns:
            Tuple of (users list, total count)
        """
        filters = [User.is_deleted == False]

        if role:
            filters.append(User.role == role)
        if is_active is not None:
            filters.append(User.is_active == is_active)

        stmt = select(User).where(and_(*filters))

        # Sort
        sort_field = getattr(User, sort_by, User.created_at)
        if sort_order.lower() == "asc":
            stmt = stmt.order_by(asc(sort_field))
        else:
            stmt = stmt.order_by(desc(sort_field))

        # Count total
        count_stmt = select(User).where(and_(*filters))
        total = len(self.db.scalars(count_stmt).all())

        # Paginate
        stmt = stmt.offset(skip).limit(limit)
        users = self.db.scalars(stmt).all()

        return users, total

    def activate_user(self, user: User) -> User:
        """Activate user.

        Args:
            user: User model instance

        Returns:
            Updated user
        """
        user.is_active = True
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate_user(self, user: User) -> User:
        """Deactivate user.

        Args:
            user: User model instance

        Returns:
            Updated user
        """
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def count_users(self) -> int:
        """Count total non-deleted users.

        Returns:
            Total user count
        """
        stmt = select(User).where(User.is_deleted == False)
        return len(self.db.scalars(stmt).all())
