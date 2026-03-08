"""Market data models."""
from datetime import datetime
from pydantic import BaseModel, Field


class Instrument(BaseModel):
    """Searchable instrument/security."""
    symbol: str = Field(description="Trading symbol (e.g., AAPL, RELIANCE.NS)")
    name: str = Field(description="Company name")
    scrip_code: str = Field(default="", description="Exchange scrip code")
    exchange: str = Field(default="", description="Exchange (NYSE/NASDAQ/BSE/NSE)")
    type: str = Field(default="equity", description="Instrument type")


class Quote(BaseModel):
    """Real-time quote for a security."""
    symbol: str
    name: str | None = None
    ltp: float = Field(description="Last traded price")
    change: float | None = Field(default=None, description="Absolute change from prev close")
    change_percent: float | None = Field(default=None, description="Percent change from prev close")
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = Field(default=None, description="Previous close")
    volume: int | None = None
    avg_volume: int | None = Field(default=None, description="Average volume")
    bid: float | None = None
    ask: float | None = None
    timestamp: datetime
    market_cap: float | None = Field(default=None, description="Market capitalization")
    pe_ratio: float | None = Field(default=None, description="Trailing P/E ratio")
    week_52_high: float | None = None
    week_52_low: float | None = None
    currency: str = Field(default="USD", description="Currency code")


class OHLCV(BaseModel):
    """OHLCV candle data."""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class HistoryRequest(BaseModel):
    """Request parameters for historical data."""
    symbol: str
    start_date: datetime
    end_date: datetime
    interval: str = Field(default="1d", pattern="^(1m|5m|15m|30m|1h|1d|1w|1M)$")
