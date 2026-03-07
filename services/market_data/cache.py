"""Cache layer for market data."""
from datetime import datetime, timedelta
from typing import Any
from pydantic import BaseModel


class CacheEntry(BaseModel):
    """Cached item with expiration."""
    data: Any
    expires_at: datetime


class MarketDataCache:
    """In-memory cache for market data.

    TTL defaults:
        - Quotes: 1 second (real-time)
        - History: 1 hour (immutable once closed)
    """

    def __init__(self):
        self._cache: dict[str, CacheEntry] = {}

    async def get(self, key: str) -> Any | None:
        """Get cached item if not expired."""
        entry = self._cache.get(key)
        if entry is None:
            return None
        if datetime.utcnow() > entry.expires_at:
            del self._cache[key]
            return None
        return entry.data

    async def set(self, key: str, data: Any, ttl_seconds: int = 1) -> None:
        """Cache item with TTL."""
        self._cache[key] = CacheEntry(
            data=data,
            expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds),
        )

    async def invalidate(self, pattern: str) -> int:
        """Invalidate keys matching pattern. Returns count invalidated."""
        keys_to_delete = [k for k in self._cache if pattern in k]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)

    async def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
