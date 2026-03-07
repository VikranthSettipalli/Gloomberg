"""FastAPI router for index endpoints."""
from fastapi import APIRouter, HTTPException

from services.models import IndexData, Constituent
from .providers.base import IndexProvider
from .providers.nse_index import NSEIndexProvider

router = APIRouter(prefix="/indices", tags=["indices"])

_provider: IndexProvider = NSEIndexProvider()


def set_provider(provider: IndexProvider) -> None:
    global _provider
    _provider = provider


@router.get("/{index_symbol}", response_model=IndexData)
async def get_index(index_symbol: str) -> IndexData:
    """Get index quote and summary."""
    try:
        return await _provider.get_index(index_symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/{index_symbol}/constituents", response_model=list[Constituent])
async def get_constituents(index_symbol: str) -> list[Constituent]:
    """Get index constituents."""
    try:
        return await _provider.get_constituents(index_symbol)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
