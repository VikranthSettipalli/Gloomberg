"""BSE shareholding provider."""
from .base import ShareholdingProvider
from services.models import Shareholding


class BSEShareholdingProvider(ShareholdingProvider):
    """BSE India shareholding provider.

    Source: BSE API quarterly shareholding filings
    Data: FII, DII, promoter, public percentages
    """

    async def get_shareholding(self, symbol: str) -> Shareholding:
        raise NotImplementedError("BSEShareholdingProvider.get_shareholding not yet implemented")

    async def get_shareholding_history(self, symbol: str) -> list[Shareholding]:
        raise NotImplementedError("BSEShareholdingProvider.get_shareholding_history not yet implemented")
