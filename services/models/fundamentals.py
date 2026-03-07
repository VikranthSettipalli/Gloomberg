"""Fundamental data models."""
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class Financials(BaseModel):
    """Quarterly/Annual financial statements."""
    symbol: str
    period: str = Field(description="Q1, Q2, Q3, Q4, or FY")
    fiscal_year: int
    revenue: Decimal | None = None
    net_income: Decimal | None = None
    ebitda: Decimal | None = None
    eps: Decimal | None = None
    total_assets: Decimal | None = None
    total_liabilities: Decimal | None = None
    total_equity: Decimal | None = None
    operating_cash_flow: Decimal | None = None
    filing_date: date | None = None


class Ratios(BaseModel):
    """Financial ratios."""
    symbol: str
    pe_ratio: Decimal | None = None
    pb_ratio: Decimal | None = None
    ps_ratio: Decimal | None = None
    ev_ebitda: Decimal | None = None
    debt_to_equity: Decimal | None = None
    current_ratio: Decimal | None = None
    roe: Decimal | None = None
    roa: Decimal | None = None
    gross_margin: Decimal | None = None
    operating_margin: Decimal | None = None
    net_margin: Decimal | None = None


class Filing(BaseModel):
    """Corporate filing metadata."""
    symbol: str
    filing_type: str
    title: str
    filing_date: date
    url: str | None = None
