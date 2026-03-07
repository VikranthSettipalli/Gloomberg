"""FastAPI router for fundamentals endpoints."""
from fastapi import APIRouter, HTTPException, Query

from services.models import Financials, Ratios, Filing
from .providers.base import FundamentalsProvider
from .providers.bse_filings import BSEFilingsProvider

router = APIRouter(prefix="/fundamentals", tags=["fundamentals"])

_provider: FundamentalsProvider = BSEFilingsProvider()


def set_provider(provider: FundamentalsProvider) -> None:
    """Set the active fundamentals provider."""
    global _provider
    _provider = provider


@router.get("/financials/{symbol}", response_model=list[Financials])
async def get_financials(
    symbol: str,
    period: str = Query("quarterly", pattern="^(quarterly|annual)$"),
) -> list[Financials]:
    """Get financial statements for a symbol."""
    try:
        return await _provider.get_financials(symbol, period)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/ratios/{symbol}", response_model=Ratios)
async def get_ratios(symbol: str) -> Ratios:
    """Get financial ratios for a symbol."""
    try:
        return await _provider.get_ratios(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/filings/{symbol}", response_model=list[Filing])
async def get_filings(
    symbol: str,
    filing_type: str | None = Query(None),
) -> list[Filing]:
    """Get corporate filings for a symbol."""
    try:
        return await _provider.get_filings(symbol, filing_type)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
