"""Tests for KiteProvider."""
import pytest
from datetime import date

from services.market_data.providers.kite import KiteProvider
from services.market_data.providers.base import MarketDataProvider


class TestKiteProvider:
    @pytest.fixture
    def provider(self) -> KiteProvider:
        return KiteProvider()

    def test_implements_interface(self, provider: KiteProvider):
        """KiteProvider should implement MarketDataProvider."""
        assert isinstance(provider, MarketDataProvider)

    @pytest.mark.asyncio
    async def test_get_quote_not_implemented(self, provider: KiteProvider):
        """get_quote raises NotImplementedError (stub)."""
        with pytest.raises(NotImplementedError):
            await provider.get_quote("RELIANCE.NS")

    @pytest.mark.asyncio
    async def test_get_history_not_implemented(self, provider: KiteProvider):
        """get_history raises NotImplementedError (stub)."""
        with pytest.raises(NotImplementedError):
            await provider.get_history(
                "RELIANCE.NS",
                date(2026, 1, 1),
                date(2026, 3, 1),
            )

    @pytest.mark.asyncio
    async def test_stream_quotes_not_implemented(self, provider: KiteProvider):
        """stream_quotes raises NotImplementedError (stub)."""
        with pytest.raises(NotImplementedError):
            async for _ in provider.stream_quotes(["RELIANCE.NS"]):
                pass
