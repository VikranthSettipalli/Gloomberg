"""FastAPI router for shareholding endpoints."""
from fastapi import APIRouter, HTTPException

from services.models import Shareholding
from .providers.base import ShareholdingProvider
from .providers.bse_shareholding import BSEShareholdingProvider

router = APIRouter(prefix="/shareholding", tags=["shareholding"])

_provider: ShareholdingProvider = BSEShareholdingProvider()


def set_provider(provider: ShareholdingProvider) -> None:
    global _provider
    _provider = provider


@router.get("/{symbol}", response_model=Shareholding)
async def get_shareholding(symbol: str) -> Shareholding:
    """Get latest shareholding pattern."""
    try:
        return await _provider.get_shareholding(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/{symbol}/history", response_model=list[Shareholding])
async def get_shareholding_history(symbol: str) -> list[Shareholding]:
    """Get historical shareholding patterns."""
    try:
        return await _provider.get_shareholding_history(symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
