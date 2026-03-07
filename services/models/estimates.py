"""Analyst estimates models."""
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class Estimate(BaseModel):
    """Single analyst estimate."""
    source: str
    value: Decimal
    date: date
    basis: str = Field(default="consolidated", pattern="^(consolidated|standalone)$")


class Consensus(BaseModel):
    """Aggregated consensus metrics."""
    mean: Decimal | None = None
    trimmed_mean: Decimal | None = None
    median: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    std_dev: Decimal | None = None
    num_estimates: int = 0
    recency_weighted_mean: Decimal | None = None


class Estimates(BaseModel):
    """Consensus estimates for a metric."""
    symbol: str
    metric: str = Field(description="EPS, Revenue, EBITDA, etc.")
    period: str = Field(description="FY2025E, Q1FY26E, etc.")
    basis: str = "consolidated"
    adjusted: bool = True
    consensus: Consensus
    individual_estimates: list[Estimate] = []
    last_updated: date | None = None


class PriceTarget(BaseModel):
    """Analyst price target."""
    source: str
    target: Decimal
    date: date
    rating: str | None = None


class PriceTargets(BaseModel):
    """Aggregated price targets."""
    symbol: str
    mean: Decimal | None = None
    median: Decimal | None = None
    high: Decimal | None = None
    low: Decimal | None = None
    num_analysts: int = 0
    targets: list[PriceTarget] = []


class Recommendation(BaseModel):
    """Analyst recommendation counts."""
    symbol: str
    strong_buy: int = 0
    buy: int = 0
    hold: int = 0
    sell: int = 0
    strong_sell: int = 0
    period: str | None = None
