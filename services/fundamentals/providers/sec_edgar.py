"""SEC EDGAR provider for US stock fundamentals."""
from .base import FundamentalsProvider
from services.models import Financials, Ratios, Filing


class SECEdgarProvider(FundamentalsProvider):
    """SEC EDGAR fundamentals provider.

    Source: SEC EDGAR API (XBRL filings)
    Cost: Free (requires User-Agent header with email)
    Coverage: All SEC-reporting US companies

    Data available:
        - 10-K, 10-Q filings (structured XBRL)
        - Financial statements
        - Company facts API
    """

    def __init__(self, user_agent_email: str | None = None):
        self.user_agent_email = user_agent_email

    async def get_financials(
        self, symbol: str, period: str = "quarterly"
    ) -> list[Financials]:
        """Get financials from SEC EDGAR XBRL."""
        raise NotImplementedError("SECEdgarProvider.get_financials not yet implemented")

    async def get_ratios(self, symbol: str) -> Ratios:
        """Calculate ratios from SEC filings."""
        raise NotImplementedError("SECEdgarProvider.get_ratios not yet implemented")

    async def get_filings(
        self, symbol: str, filing_type: str | None = None
    ) -> list[Filing]:
        """Get filings index from SEC EDGAR."""
        raise NotImplementedError("SECEdgarProvider.get_filings not yet implemented")
