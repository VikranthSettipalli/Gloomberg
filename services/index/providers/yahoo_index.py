"""Yahoo Finance index provider."""
from .base import IndexProvider
from services.models import IndexData, Constituent


class YahooIndexProvider(IndexProvider):
    """Yahoo Finance index provider.

    Coverage: S&P 500, global indices
    """

    async def get_index(self, index_symbol: str) -> IndexData:
        raise NotImplementedError("YahooIndexProvider.get_index not yet implemented")

    async def get_constituents(self, index_symbol: str) -> list[Constituent]:
        raise NotImplementedError("YahooIndexProvider.get_constituents not yet implemented")
