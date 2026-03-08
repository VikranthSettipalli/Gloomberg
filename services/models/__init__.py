"""Shared Pydantic models for all services."""
from .market import Quote, OHLCV, HistoryRequest, Instrument
from .fundamentals import (
    Financials, Ratios, Filing, CompanyProfile,
    IncomeStatement, BalanceSheet, CashFlowStatement,
)
from .index import IndexData, Constituent
from .estimates import Estimate, Consensus, Estimates, PriceTarget, PriceTargets, Recommendation
from .shareholding import Shareholding, ShareholdingCategory

__all__ = [
    # Market
    "Quote",
    "OHLCV",
    "HistoryRequest",
    "Instrument",
    # Fundamentals
    "Financials",
    "Ratios",
    "Filing",
    "CompanyProfile",
    "IncomeStatement",
    "BalanceSheet",
    "CashFlowStatement",
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
