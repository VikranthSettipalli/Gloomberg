"""Tests for YahooProvider."""
import pytest
from datetime import date

from services.market_data.providers.yahoo import YahooProvider
from services.market_data.providers.base import MarketDataProvider


class TestYahooProvider:
    @pytest.fixture
    def provider(self) -> YahooProvider:
        return YahooProvider()

    def test_implements_interface(self, provider: YahooProvider):
        """YahooProvider should implement MarketDataProvider."""
        assert isinstance(provider, MarketDataProvider)

    @pytest.mark.asyncio
    async def test_get_quote_not_implemented(self, provider: YahooProvider):
        """get_quote raises NotImplementedError (stub)."""
        with pytest.raises(NotImplementedError):
            await provider.get_quote("AAPL")

    @pytest.mark.asyncio
    async def test_get_history_not_implemented(self, provider: YahooProvider):
        """get_history raises NotImplementedError (stub)."""
        with pytest.raises(NotImplementedError):
            await provider.get_history(
                "AAPL",
                date(2026, 1, 1),
                date(2026, 3, 1),
            )

    @pytest.mark.asyncio
    async def test_stream_quotes_not_supported(self, provider: YahooProvider):
        """stream_quotes not supported by Yahoo."""
        with pytest.raises(NotImplementedError, match="does not support"):
            async for _ in provider.stream_quotes(["AAPL"]):
                pass
