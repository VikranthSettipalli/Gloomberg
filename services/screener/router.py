"""FastAPI router for screener endpoints."""
from fastapi import APIRouter, HTTPException

from .engine import ScreenerEngine, ScreenerQuery, ScreenerResult

router = APIRouter(prefix="/screener", tags=["screener"])

_engine = ScreenerEngine()


@router.post("/screen", response_model=list[ScreenerResult])
async def screen(query: ScreenerQuery) -> list[ScreenerResult]:
    """Execute equity screening query."""
    try:
        return await _engine.screen(query)
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.get("/fields", response_model=list[str])
async def get_fields() -> list[str]:
    """Get available screening fields."""
    try:
        return await _engine.get_available_fields()
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
