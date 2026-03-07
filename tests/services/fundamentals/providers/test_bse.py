"""Tests for BSEFilingsProvider."""
import pytest

from services.fundamentals.providers.bse_filings import BSEFilingsProvider
from services.fundamentals.providers.base import FundamentalsProvider


class TestBSEFilingsProvider:
    @pytest.fixture
    def provider(self) -> BSEFilingsProvider:
        return BSEFilingsProvider()

    def test_implements_interface(self, provider: BSEFilingsProvider):
        assert isinstance(provider, FundamentalsProvider)

    @pytest.mark.asyncio
    async def test_get_financials_not_implemented(self, provider: BSEFilingsProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_financials("RELIANCE")

    @pytest.mark.asyncio
    async def test_get_ratios_not_implemented(self, provider: BSEFilingsProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_ratios("RELIANCE")

    @pytest.mark.asyncio
    async def test_get_filings_not_implemented(self, provider: BSEFilingsProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_filings("RELIANCE")
