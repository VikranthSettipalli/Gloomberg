"""Financial Modeling Prep estimates provider."""
from .base import EstimatesProvider
from services.models import Estimates, PriceTargets, Recommendation


class FMPProvider(EstimatesProvider):
    """Financial Modeling Prep estimates provider.

    Free tier: 250 calls/day
    Coverage: Strong for US equities, limited for pure Indian stocks
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def get_estimates(self, symbol: str) -> Estimates:
        raise NotImplementedError("FMPProvider.get_estimates not yet implemented")

    async def get_price_targets(self, symbol: str) -> PriceTargets:
        raise NotImplementedError("FMPProvider.get_price_targets not yet implemented")

    async def get_recommendations(self, symbol: str) -> Recommendation:
        raise NotImplementedError("FMPProvider.get_recommendations not yet implemented")
