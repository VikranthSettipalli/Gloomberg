"""Tests for FMPProvider."""
import pytest

from services.estimates.providers.fmp import FMPProvider
from services.estimates.providers.base import EstimatesProvider


class TestFMPProvider:
    @pytest.fixture
    def provider(self) -> FMPProvider:
        return FMPProvider()

    def test_implements_interface(self, provider: FMPProvider):
        assert isinstance(provider, EstimatesProvider)

    @pytest.mark.asyncio
    async def test_get_estimates_not_implemented(self, provider: FMPProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_estimates("AAPL")

    @pytest.mark.asyncio
    async def test_get_price_targets_not_implemented(self, provider: FMPProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_price_targets("AAPL")

    @pytest.mark.asyncio
    async def test_get_recommendations_not_implemented(self, provider: FMPProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_recommendations("AAPL")
