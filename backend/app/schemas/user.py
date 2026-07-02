"""User Pydantic schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserCreate(BaseModel):
    """User creation schema."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.STUDENT

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "phone": "+1234567890",
                "role": "student",
            }
        }


class UserUpdate(BaseModel):
    """User update schema."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = None
    profile_image: Optional[str] = Field(None, max_length=500)

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "full_name": "Jane Doe",
                "phone": "+1234567890",
                "bio": "Software engineer and educator",
                "profile_image": "https://example.com/profile.jpg",
            }
        }


class UserResponse(BaseModel):
    """User response schema."""

    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    role: UserRole
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserProfile(BaseModel):
    """User profile schema."""

    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserListResponse(BaseModel):
    """User list item response schema."""

    user_id: str
    full_name: str
    email: str
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class UserFilter(BaseModel):
    """User filter schema."""

    search: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    sort_by: str = "created_at"
    sort_order: str = "desc"

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "search": "john",
                "role": "student",
                "is_active": True,
                "sort_by": "created_at",
                "sort_order": "desc",
            }
        }


class PaginationResponse(BaseModel):
    """Pagination response schema."""

    total_records: int
    total_pages: int
    current_page: int
    page_size: int
    items: list[UserListResponse]

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "total_records": 100,
                "total_pages": 5,
                "current_page": 1,
                "page_size": 20,
                "items": [],
            }
        }
