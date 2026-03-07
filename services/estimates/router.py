"""FastAPI router for estimates endpoints."""
from fastapi import APIRouter, HTTPException

from services.models import Estimates, PriceTargets, Recommendation
from .providers.base import EstimatesProvider
from .providers.fmp import FMPProvider

router = APIRouter(prefix="/estimates", tags=["estimates"])

_provider: EstimatesProvider = FMPProvider()


def set_provider(provider: EstimatesProvider) -> None:
    global _provider
    _provider = provider


@router.get("/{symbol}", response_model=Estimates)
async def get_estimates(symbol: str) -> Estimates:
    """Get consensus estimates for a symbol."""
    try:
        return await _provider.get_estimates(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/{symbol}/price-targets", response_model=PriceTargets)
async def get_price_targets(symbol: str) -> PriceTargets:
    """Get analyst price targets."""
    try:
        return await _provider.get_price_targets(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/{symbol}/recommendations", response_model=Recommendation)
async def get_recommendations(symbol: str) -> Recommendation:
    """Get buy/hold/sell recommendations."""
    try:
        return await _provider.get_recommendations(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
