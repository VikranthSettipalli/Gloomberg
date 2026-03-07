"""Tests for NSEIndexProvider."""
import pytest

from services.index.providers.nse_index import NSEIndexProvider
from services.index.providers.base import IndexProvider


class TestNSEIndexProvider:
    @pytest.fixture
    def provider(self) -> NSEIndexProvider:
        return NSEIndexProvider()

    def test_implements_interface(self, provider: NSEIndexProvider):
        assert isinstance(provider, IndexProvider)

    @pytest.mark.asyncio
    async def test_get_index_not_implemented(self, provider: NSEIndexProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_index("NIFTY50")

    @pytest.mark.asyncio
    async def test_get_constituents_not_implemented(self, provider: NSEIndexProvider):
        with pytest.raises(NotImplementedError):
            await provider.get_constituents("NIFTY50")
