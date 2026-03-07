"""Zerodha Kite Connect provider for real-time market data."""
from datetime import date
from typing import AsyncIterator

from .base import MarketDataProvider
from services.models import Quote, OHLCV


class KiteProvider(MarketDataProvider):
    """Zerodha Kite Connect market data provider.

    Requires:
        - KITE_API_KEY
        - KITE_API_SECRET
        - Daily OAuth token refresh

    Capabilities:
        - Real-time streaming via WebSocket
        - Up to 3,000 instrument subscriptions
        - Historical candles (1min to daily)
        - 5-level bid/ask depth
    """

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        self.api_key = api_key
        self.api_secret = api_secret

    async def get_quote(self, symbol: str) -> Quote:
        """Get real-time quote from Kite."""
        raise NotImplementedError("KiteProvider.get_quote not yet implemented")

    async def get_history(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """Get historical data from Kite."""
        raise NotImplementedError("KiteProvider.get_history not yet implemented")

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        """Stream quotes via Kite WebSocket."""
        raise NotImplementedError("KiteProvider.stream_quotes not yet implemented")
        yield  # type: ignore  # Make this a generator
