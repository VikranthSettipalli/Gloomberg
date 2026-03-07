"""Abstract base class for fundamentals providers."""
from abc import ABC, abstractmethod

from services.models import Financials, Ratios, Filing


class FundamentalsProvider(ABC):
    """Base interface for fundamentals providers.

    All fundamentals providers must implement this interface.
    Providers: BSE (India), SEC EDGAR (US).
    """

    @abstractmethod
    async def get_financials(
        self, symbol: str, period: str = "quarterly"
    ) -> list[Financials]:
        """Get financial statements.

        Args:
            symbol: Stock symbol
            period: "quarterly" or "annual"

        Returns:
            List of financial statements
        """
        ...

    @abstractmethod
    async def get_ratios(self, symbol: str) -> Ratios:
        """Get current financial ratios.

        Args:
            symbol: Stock symbol

        Returns:
            Financial ratios (PE, PB, margins, etc.)
        """
        ...

    @abstractmethod
    async def get_filings(
        self, symbol: str, filing_type: str | None = None
    ) -> list[Filing]:
        """Get corporate filings.

        Args:
            symbol: Stock symbol
            filing_type: Filter by type (e.g., "10-K", "quarterly")

        Returns:
            List of filing metadata
        """
        ...
