"""Market data models."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class Quote(BaseModel):
    """Real-time quote for a security."""
    symbol: str
    ltp: Decimal = Field(description="Last traded price")
    open: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    close: Decimal | None = None
    volume: int | None = None
    bid: Decimal | None = None
    ask: Decimal | None = None
    timestamp: datetime


class OHLCV(BaseModel):
    """OHLCV candle data."""
    symbol: str
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class HistoryRequest(BaseModel):
    """Request parameters for historical data."""
    symbol: str
    start_date: datetime
    end_date: datetime
    interval: str = Field(default="1d", pattern="^(1m|5m|15m|30m|1h|1d|1w|1M)$")
