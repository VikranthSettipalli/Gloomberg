"""Finnhub estimates provider."""
from .base import EstimatesProvider
from services.models import Estimates, PriceTargets, Recommendation


class FinnhubProvider(EstimatesProvider):
    """Finnhub estimates provider (supplementary).

    Free tier: 60 calls/min
    Free data: Recommendation trends, earnings surprises
    Premium only: EPS/revenue estimates, price targets
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def get_estimates(self, symbol: str) -> Estimates:
        raise NotImplementedError("FinnhubProvider.get_estimates not yet implemented (requires premium)")

    async def get_price_targets(self, symbol: str) -> PriceTargets:
        raise NotImplementedError("FinnhubProvider.get_price_targets not yet implemented (requires premium)")

    async def get_recommendations(self, symbol: str) -> Recommendation:
        raise NotImplementedError("FinnhubProvider.get_recommendations not yet implemented")
