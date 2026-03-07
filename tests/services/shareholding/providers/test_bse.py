"""Tests for BSEShareholdingProvider."""
import pytest

from services.shareholding.providers.bse_shareholding import BSEShareholdingProvider
from services.shareholding.providers.base import ShareholdingProvider


class TestBSEShareholdingProvider:
    @pytest.fixture
    def provider(self) -> BSEShareholdingProvider:
        return BSEShareholdingProvider()

    def test_implements_interface(self, provider: BSEShareholdingProvider):
        assert isinstance(provider, ShareholdingProvider)

    @pytest.mark.asyncio
    async def test_get_shareholding_not_implemented(self, provider: BSEShareholdingProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_shareholding("RELIANCE")

    @pytest.mark.asyncio
    async def test_get_shareholding_history_not_implemented(self, provider: BSEShareholdingProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_shareholding_history("RELIANCE")
