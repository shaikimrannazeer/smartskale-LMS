"""Request logging middleware."""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and response times."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request and log details.

        Args:
            request: HTTP request
            call_next: Next middleware/route handler

        Returns:
            HTTP response
        """
        # Record start time
        start_time = time.time()

        # Get request details
        method = request.method
        path = request.url.path
        query_params = dict(request.query_params)

        # Process request
        response = await call_next(request)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Log request details
        logger.info(
            f"{method} {path} - Status: {response.status_code} - "
            f"Execution Time: {execution_time:.3f}s"
        )

        # Add execution time to response headers
        response.headers["X-Process-Time"] = str(execution_time)

        return response
