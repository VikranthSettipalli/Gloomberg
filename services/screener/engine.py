"""Equity screening engine."""
from pydantic import BaseModel
from typing import Any


class ScreenerFilter(BaseModel):
    """Single filter condition."""
    field: str
    operator: str  # eq, ne, gt, lt, gte, lte, in, between
    value: Any


class ScreenerQuery(BaseModel):
    """Screener query with filters and sorting."""
    filters: list[ScreenerFilter] = []
    sort_by: str | None = None
    sort_order: str = "desc"
    limit: int = 50
    offset: int = 0


class ScreenerResult(BaseModel):
    """Screener result row."""
    symbol: str
    name: str | None = None
    data: dict[str, Any] = {}


class ScreenerEngine:
    """Equity screening engine.

    Filters and sorts stocks based on multiple criteria.
    Uses cached/precomputed metrics from other services.
    """

    async def screen(self, query: ScreenerQuery) -> list[ScreenerResult]:
        """Execute screening query."""
        raise NotImplementedError("ScreenerEngine.screen not yet implemented")

    async def get_available_fields(self) -> list[str]:
        """Get list of fields available for filtering."""
        raise NotImplementedError("ScreenerEngine.get_available_fields not yet implemented")
