"""FastAPI router for market data endpoints."""
from datetime import date
from fastapi import APIRouter, HTTPException, Query

from services.models import Quote, OHLCV
from .providers.base import MarketDataProvider
from .providers.yahoo import YahooProvider

router = APIRouter(prefix="/market", tags=["market"])

# Default provider (configured via gateway)
_provider: MarketDataProvider = YahooProvider()


def set_provider(provider: MarketDataProvider) -> None:
    """Set the active market data provider."""
    global _provider
    _provider = provider


@router.get("/quote/{symbol}", response_model=Quote)
async def get_quote(symbol: str) -> Quote:
    """Get real-time quote for a symbol.

    Args:
        symbol: Stock symbol (e.g., RELIANCE.NS, AAPL)
    """
    try:
        return await _provider.get_quote(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/history/{symbol}", response_model=list[OHLCV])
async def get_history(
    symbol: str,
    start: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end: date = Query(..., description="End date (YYYY-MM-DD)"),
    interval: str = Query("1d", pattern="^(1m|5m|15m|30m|1h|1d|1w|1M)$"),
) -> list[OHLCV]:
    """Get historical OHLCV data.

    Args:
        symbol: Stock symbol
        start: Start date
        end: End date
        interval: Candle interval
    """
    try:
        return await _provider.get_history(symbol, start, end, interval)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
