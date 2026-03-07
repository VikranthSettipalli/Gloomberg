"""Abstract base class for index providers."""
from abc import ABC, abstractmethod

from services.models import IndexData, Constituent


class IndexProvider(ABC):
    """Base interface for index providers.

    Providers: NSE (India), Yahoo (global).
    """

    @abstractmethod
    async def get_index(self, index_symbol: str) -> IndexData:
        """Get index quote and summary."""
        ...

    @abstractmethod
    async def get_constituents(self, index_symbol: str) -> list[Constituent]:
        """Get index constituents with weights."""
        ...
