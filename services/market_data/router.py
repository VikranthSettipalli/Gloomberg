"""FastAPI router for market data endpoints."""
from datetime import date
from fastapi import APIRouter, HTTPException, Query

from services.models import (
    Quote, OHLCV, Instrument, Ratios, CompanyProfile,
    IncomeStatement, BalanceSheet, CashFlowStatement,
)
from .providers.yahoo import YahooProvider

router = APIRouter(prefix="/market", tags=["market"])

# Default provider - Yahoo Finance for global coverage
_provider = YahooProvider()


@router.get("/search", response_model=list[Instrument])
async def search_instruments(
    q: str = Query(..., min_length=1, description="Search query")
) -> list[Instrument]:
    """Search for instruments by name or symbol."""
    try:
        return await _provider.search(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quote/{symbol:path}", response_model=Quote)
async def get_quote(symbol: str) -> Quote:
    """Get quote for a symbol (e.g., AAPL, RELIANCE.NS)."""
    try:
        return await _provider.get_quote(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{symbol:path}", response_model=list[OHLCV])
async def get_history(
    symbol: str,
    start: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end: date = Query(..., description="End date (YYYY-MM-DD)"),
    interval: str = Query("1d", pattern="^(1m|5m|15m|30m|1h|1d|1w|1M)$"),
) -> list[OHLCV]:
    """Get historical OHLCV data."""
    try:
        return await _provider.get_history(symbol, start, end, interval)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{symbol:path}", response_model=CompanyProfile)
async def get_profile(symbol: str) -> CompanyProfile:
    """Get company profile information."""
    try:
        return await _provider.get_company_profile(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ratios/{symbol:path}", response_model=Ratios)
async def get_ratios(symbol: str) -> Ratios:
    """Get financial ratios and valuation multiples."""
    try:
        return await _provider.get_ratios(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/income-statement/{symbol:path}", response_model=list[IncomeStatement])
async def get_income_statements(
    symbol: str,
    period: str = Query("annual", pattern="^(annual|quarterly)$"),
) -> list[IncomeStatement]:
    """Get income statements."""
    try:
        return await _provider.get_income_statements(symbol, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance-sheet/{symbol:path}", response_model=list[BalanceSheet])
async def get_balance_sheets(
    symbol: str,
    period: str = Query("annual", pattern="^(annual|quarterly)$"),
) -> list[BalanceSheet]:
    """Get balance sheets."""
    try:
        return await _provider.get_balance_sheets(symbol, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cash-flow/{symbol:path}", response_model=list[CashFlowStatement])
async def get_cash_flow(
    symbol: str,
    period: str = Query("annual", pattern="^(annual|quarterly)$"),
) -> list[CashFlowStatement]:
    """Get cash flow statements."""
    try:
        return await _provider.get_cash_flow_statements(symbol, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
