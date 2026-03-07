"""NSE India index provider."""
from .base import IndexProvider
from services.models import IndexData, Constituent


class NSEIndexProvider(IndexProvider):
    """NSE India index provider.

    Source: NSE official endpoints
    Coverage: Nifty 50, sectoral indices, all NSE indices
    """

    async def get_index(self, index_symbol: str) -> IndexData:
        raise NotImplementedError("NSEIndexProvider.get_index not yet implemented")

    async def get_constituents(self, index_symbol: str) -> list[Constituent]:
        raise NotImplementedError("NSEIndexProvider.get_constituents not yet implemented")
