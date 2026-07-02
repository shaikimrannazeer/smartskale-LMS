"""Custom exception classes for the application."""

from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize exception.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Application error code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Validation error exception."""

    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize validation error.

        Args:
            message: Error message
            details: Validation error details
        """
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class NotFoundError(AppException):
    """Resource not found exception."""

    def __init__(
        self,
        message: str = "Resource not found",
        resource: Optional[str] = None,
    ) -> None:
        """Initialize not found error.

        Args:
            message: Error message
            resource: Resource type
        """
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details={"resource": resource} if resource else {},
        )


class UnauthorizedError(AppException):
    """Unauthorized access exception."""

    def __init__(self, message: str = "Unauthorized") -> None:
        """Initialize unauthorized error.

        Args:
            message: Error message
        """
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED",
        )


class ForbiddenError(AppException):
    """Forbidden access exception."""

    def __init__(self, message: str = "Forbidden") -> None:
        """Initialize forbidden error.

        Args:
            message: Error message
        """
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN",
        )


class ConflictError(AppException):
    """Conflict error exception."""

    def __init__(self, message: str = "Conflict") -> None:
        """Initialize conflict error.

        Args:
            message: Error message
        """
        super().__init__(
            message=message,
            status_code=409,
            error_code="CONFLICT",
        )
