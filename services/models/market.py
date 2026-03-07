"""Market data models."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class Instrument(BaseModel):
    """Searchable instrument/security."""
    symbol: str = Field(description="Trading symbol (e.g., RELIANCE)")
    name: str = Field(description="Company name")
    scrip_code: str = Field(description="Exchange scrip code (e.g., 500325)")
    exchange: str = Field(default="BSE", description="Exchange (BSE/NSE)")


class Quote(BaseModel):
    """Real-time quote for a security."""
    symbol: str
    name: str | None = None
    ltp: Decimal = Field(description="Last traded price")
    change: Decimal | None = Field(default=None, description="Absolute change from prev close")
    change_percent: Decimal | None = Field(default=None, description="Percent change from prev close")
    open: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    close: Decimal | None = Field(default=None, description="Previous close")
    volume: int | None = None
    avg_volume: int | None = Field(default=None, description="Average volume")
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
