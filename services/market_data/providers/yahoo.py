"""Yahoo Finance provider for free market data (fallback)."""
from datetime import date
from typing import AsyncIterator

from .base import MarketDataProvider
from services.models import Quote, OHLCV


class YahooProvider(MarketDataProvider):
    """Yahoo Finance market data provider (free fallback).

    Requires: No API key (uses yfinance library)

    Limitations:
        - ~15 minute delay on quotes
        - No real-time streaming
        - Unofficial API (~2000 requests/hour)

    Good for:
        - Historical OHLCV data
        - US/global stock coverage
        - Development/testing
    """

    async def get_quote(self, symbol: str) -> Quote:
        """Get delayed quote from Yahoo Finance."""
        raise NotImplementedError("YahooProvider.get_quote not yet implemented")

    async def get_history(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """Get historical data from Yahoo Finance."""
        raise NotImplementedError("YahooProvider.get_history not yet implemented")

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        """Yahoo does not support streaming - raises error."""
        raise NotImplementedError("YahooProvider does not support real-time streaming")
        yield  # type: ignore  # Make this a generator
