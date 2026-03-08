"""Fundamental data models."""
from datetime import date
from pydantic import BaseModel, Field


class IncomeStatement(BaseModel):
    """Income statement line items."""
    symbol: str
    period: str = Field(description="quarterly or annual")
    date: date
    fiscal_year: int | None = None
    revenue: float | None = None
    cost_of_revenue: float | None = None
    gross_profit: float | None = None
    operating_expenses: float | None = None
    operating_income: float | None = None
    ebitda: float | None = None
    interest_expense: float | None = None
    income_before_tax: float | None = None
    income_tax: float | None = None
    net_income: float | None = None
    eps: float | None = None
    eps_diluted: float | None = None
    shares_outstanding: float | None = None
    # Margins (computed)
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None


class BalanceSheet(BaseModel):
    """Balance sheet line items."""
    symbol: str
    period: str
    date: date
    fiscal_year: int | None = None
    # Assets
    cash_and_equivalents: float | None = None
    short_term_investments: float | None = None
    receivables: float | None = None
    inventory: float | None = None
    total_current_assets: float | None = None
    property_plant_equipment: float | None = None
    goodwill: float | None = None
    intangible_assets: float | None = None
    total_assets: float | None = None
    # Liabilities
    accounts_payable: float | None = None
    short_term_debt: float | None = None
    total_current_liabilities: float | None = None
    long_term_debt: float | None = None
    total_liabilities: float | None = None
    # Equity
    total_equity: float | None = None
    retained_earnings: float | None = None


class CashFlowStatement(BaseModel):
    """Cash flow statement line items."""
    symbol: str
    period: str
    date: date
    fiscal_year: int | None = None
    # Operating
    net_income: float | None = None
    depreciation: float | None = None
    change_in_working_capital: float | None = None
    operating_cash_flow: float | None = None
    # Investing
    capex: float | None = None
    acquisitions: float | None = None
    investing_cash_flow: float | None = None
    # Financing
    debt_issued: float | None = None
    debt_repaid: float | None = None
    dividends_paid: float | None = None
    share_buyback: float | None = None
    financing_cash_flow: float | None = None
    # Derived
    free_cash_flow: float | None = None


class Financials(BaseModel):
    """Quarterly/Annual financial statements (legacy compat)."""
    symbol: str
    period: str = Field(description="Q1, Q2, Q3, Q4, or FY")
    fiscal_year: int
    revenue: float | None = None
    net_income: float | None = None
    ebitda: float | None = None
    eps: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_equity: float | None = None
    operating_cash_flow: float | None = None
    filing_date: date | None = None


class Ratios(BaseModel):
    """Financial ratios and valuation multiples."""
    symbol: str
    # Valuation - Backward
    pe_ratio: float | None = None
    pb_ratio: float | None = None
    ps_ratio: float | None = None
    ev_ebitda: float | None = None
    ev_sales: float | None = None
    # Valuation - Forward
    forward_pe: float | None = None
    forward_ev_ebitda: float | None = None
    peg_ratio: float | None = None
    # Profitability
    roe: float | None = None
    roic: float | None = None
    roa: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    # Leverage
    debt_to_equity: float | None = None
    current_ratio: float | None = None
    # Per Share
    revenue_per_share: float | None = None
    book_value_per_share: float | None = None
    # Enterprise Value
    enterprise_value: float | None = None
    market_cap: float | None = None


class CompanyProfile(BaseModel):
    """Company overview information."""
    symbol: str
    name: str
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    exchange: str | None = None
    currency: str | None = None
    market_cap: float | None = None
    employees: int | None = None
    description: str | None = None
    website: str | None = None


class Filing(BaseModel):
    """Corporate filing metadata."""
    symbol: str
    filing_type: str
    title: str
    filing_date: date
    url: str | None = None
