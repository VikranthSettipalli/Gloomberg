"""Shared Pydantic models for all services."""
from .market import Quote, OHLCV, HistoryRequest
from .fundamentals import Financials, Ratios, Filing
from .index import IndexData, Constituent
from .estimates import Estimate, Consensus, Estimates, PriceTarget, PriceTargets, Recommendation
from .shareholding import Shareholding, ShareholdingCategory

__all__ = [
    # Market
    "Quote",
    "OHLCV",
    "HistoryRequest",
    # Fundamentals
    "Financials",
    "Ratios",
    "Filing",
    # Index
    "IndexData",
    "Constituent",
    # Estimates
    "Estimate",
    "Consensus",
    "Estimates",
    "PriceTarget",
    "PriceTargets",
    "Recommendation",
    # Shareholding
    "Shareholding",
    "ShareholdingCategory",
]
