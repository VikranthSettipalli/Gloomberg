"""Abstract base class for shareholding providers."""
from abc import ABC, abstractmethod

from services.models import Shareholding


class ShareholdingProvider(ABC):
    """Base interface for shareholding providers."""

    @abstractmethod
    async def get_shareholding(self, symbol: str) -> Shareholding:
        """Get latest shareholding pattern."""
        ...

    @abstractmethod
    async def get_shareholding_history(self, symbol: str) -> list[Shareholding]:
        """Get historical shareholding patterns."""
        ...
