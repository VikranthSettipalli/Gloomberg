"""Gateway middleware."""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class TimingMiddleware(BaseHTTPMiddleware):
    """Add response timing header."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        response.headers["X-Response-Time"] = f"{elapsed:.3f}s"
        return response
