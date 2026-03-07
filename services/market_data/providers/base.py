"""Abstract base class for market data providers."""
from abc import ABC, abstractmethod
from datetime import date
from typing import AsyncIterator

from services.models import Quote, OHLCV


class MarketDataProvider(ABC):
    """Base interface for market data providers.

    All market data providers must implement this interface.
    Providers: Kite (real-time), Yahoo (free fallback).
    """

    @abstractmethod
    async def get_quote(self, symbol: str) -> Quote:
        """Get real-time quote for a symbol.

        Args:
            symbol: Stock symbol (e.g., "RELIANCE.NS", "AAPL")

        Returns:
            Quote with LTP, OHLC, volume, bid/ask
        """
        ...

    @abstractmethod
    async def get_history(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """Get historical OHLCV data.

        Args:
            symbol: Stock symbol
            start: Start date
            end: End date
            interval: Candle interval (1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M)

        Returns:
            List of OHLCV candles
        """
        ...

    @abstractmethod
    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        """Stream real-time quotes for multiple symbols.

        Args:
            symbols: List of stock symbols to subscribe

        Yields:
            Quote updates as they arrive
        """
        ...
