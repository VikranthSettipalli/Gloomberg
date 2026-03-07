"""Abstract base class for estimates providers."""
from abc import ABC, abstractmethod

from services.models import Estimates, PriceTargets, Recommendation


class EstimatesProvider(ABC):
    """Base interface for analyst estimates providers.

    Providers: FMP (primary), Finnhub (supplementary).
    """

    @abstractmethod
    async def get_estimates(self, symbol: str) -> Estimates:
        """Get consensus estimates (EPS, revenue)."""
        ...

    @abstractmethod
    async def get_price_targets(self, symbol: str) -> PriceTargets:
        """Get analyst price targets."""
        ...

    @abstractmethod
    async def get_recommendations(self, symbol: str) -> Recommendation:
        """Get buy/hold/sell recommendations."""
        ...
