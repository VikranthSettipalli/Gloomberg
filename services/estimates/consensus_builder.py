"""Consensus builder for Indian stock estimates.

Implements like-to-like normalization rules from CLAUDE.md:
- Consolidated vs Standalone filtering
- Fiscal year alignment
- Stock split adjustments
- Recency weighting
- Outlier handling (trimmed mean)
"""
from datetime import date
from decimal import Decimal
from services.models import Estimate, Consensus, Estimates


class ConsensusBuilder:
    """Build normalized consensus from individual analyst estimates."""

    def __init__(self, half_life_days: int = 60):
        self.half_life_days = half_life_days

    def build_consensus(
        self,
        symbol: str,
        metric: str,
        period: str,
        estimates: list[Estimate],
        basis: str = "consolidated",
    ) -> Estimates:
        """Build consensus from individual estimates.

        Applies:
        - Basis filtering (consolidated/standalone)
        - Recency weighting (exponential decay)
        - Outlier removal (trimmed mean if N >= 5)
        """
        raise NotImplementedError("ConsensusBuilder.build_consensus not yet implemented")

    def _calculate_recency_weight(self, estimate_date: date, as_of: date) -> Decimal:
        """Calculate recency weight using exponential decay."""
        raise NotImplementedError("_calculate_recency_weight not yet implemented")

    def _trimmed_mean(self, values: list[Decimal], trim_pct: float = 0.1) -> Decimal:
        """Calculate trimmed mean, dropping top/bottom percentiles."""
        raise NotImplementedError("_trimmed_mean not yet implemented")
