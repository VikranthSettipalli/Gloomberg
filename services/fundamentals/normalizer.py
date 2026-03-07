"""Normalize fundamentals data across providers."""
from services.models import Financials, Ratios


class FundamentalsNormalizer:
    """Normalize fundamentals data to common schema.

    BSE and SEC EDGAR have different field names and structures.
    This normalizer maps them to the shared Financials/Ratios models.
    """

    @staticmethod
    def normalize_indian_to_common(data: dict) -> Financials:
        """Normalize Indian (BSE) financials to common format."""
        raise NotImplementedError("normalize_indian_to_common not yet implemented")

    @staticmethod
    def normalize_us_to_common(data: dict) -> Financials:
        """Normalize US (SEC) financials to common format."""
        raise NotImplementedError("normalize_us_to_common not yet implemented")

    @staticmethod
    def calculate_ratios(financials: list[Financials], price: float) -> Ratios:
        """Calculate ratios from financials and current price."""
        raise NotImplementedError("calculate_ratios not yet implemented")
