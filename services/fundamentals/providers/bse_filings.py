"""BSE India provider for Indian stock fundamentals."""
from .base import FundamentalsProvider
from services.models import Financials, Ratios, Filing


class BSEFilingsProvider(FundamentalsProvider):
    """BSE India fundamentals provider.

    Source: bseindia.com public JSON API
    Cost: Free
    Coverage: All BSE-listed Indian companies

    Data available:
        - Quarterly/Annual financials
        - Corporate announcements
        - Structured XBRL filings
    """

    async def get_financials(
        self, symbol: str, period: str = "quarterly"
    ) -> list[Financials]:
        """Get financials from BSE API."""
        raise NotImplementedError("BSEFilingsProvider.get_financials not yet implemented")

    async def get_ratios(self, symbol: str) -> Ratios:
        """Calculate ratios from BSE financials."""
        raise NotImplementedError("BSEFilingsProvider.get_ratios not yet implemented")

    async def get_filings(
        self, symbol: str, filing_type: str | None = None
    ) -> list[Filing]:
        """Get corporate filings from BSE."""
        raise NotImplementedError("BSEFilingsProvider.get_filings not yet implemented")
