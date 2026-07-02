"""Response formatting utilities."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standard API response model."""

    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": None,
                "error_code": None,
                "details": None,
            }
        }


def success_response(
    message: str = "Success",
    data: Optional[Any] = None,
) -> APIResponse:
    """Create a success response.

    Args:
        message: Response message
        data: Response data

    Returns:
        APIResponse
    """
    return APIResponse(
        success=True,
        message=message,
        data=data,
    )


def error_response(
    message: str = "Error",
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> APIResponse:
    """Create an error response.

    Args:
        message: Error message
        error_code: Error code
        details: Error details

    Returns:
        APIResponse
    """
    return APIResponse(
        success=False,
        message=message,
        error_code=error_code,
        details=details,
    )
