"""Tests for SECEdgarProvider."""
import pytest

from services.fundamentals.providers.sec_edgar import SECEdgarProvider
from services.fundamentals.providers.base import FundamentalsProvider


class TestSECEdgarProvider:
    @pytest.fixture
    def provider(self) -> SECEdgarProvider:
        return SECEdgarProvider()

    def test_implements_interface(self, provider: SECEdgarProvider):
        assert isinstance(provider, FundamentalsProvider)

    @pytest.mark.asyncio
    async def test_get_financials_not_implemented(self, provider: SECEdgarProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_financials("AAPL")

    @pytest.mark.asyncio
    async def test_get_ratios_not_implemented(self, provider: SECEdgarProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_ratios("AAPL")

    @pytest.mark.asyncio
    async def test_get_filings_not_implemented(self, provider: SECEdgarProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_filings("AAPL")
