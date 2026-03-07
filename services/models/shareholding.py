"""Shareholding pattern models."""
from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class ShareholdingCategory(BaseModel):
    """Shareholding for a category."""
    category: str
    percentage: Decimal
    shares: int | None = None


class Shareholding(BaseModel):
    """Quarterly shareholding pattern."""
    symbol: str
    quarter: str
    year: int
    filing_date: date | None = None
    promoter: Decimal | None = None
    fii: Decimal | None = None
    dii: Decimal | None = None
    public: Decimal | None = None
    others: Decimal | None = None
    categories: list[ShareholdingCategory] = []
