"""User Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole


class UserCreate(BaseModel):
    """User creation schema."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.STUDENT

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john@example.com",
                "password": "securepassword123",
                "role": "student",
            }
        }


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "securepassword123",
            }
        }


class UserResponse(BaseModel):
    """User response schema."""

    user_id: str
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class CurrentUserResponse(BaseModel):
    """Current user response schema."""

    user_id: str
    full_name: str
    email: str
    role: UserRole
    is_active: bool

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: CurrentUserResponse

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "user_id": "123e4567-e89b-12d3-a456-426614174000",
                    "full_name": "John Doe",
                    "email": "john@example.com",
                    "role": "student",
                    "is_active": True,
                },
            }
        }


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""

    refresh_token: str

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }
