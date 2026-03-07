"""Tests for ScreenerEngine."""
import pytest

from services.screener.engine import ScreenerEngine, ScreenerQuery


class TestScreenerEngine:
    @pytest.fixture
    def engine(self) -> ScreenerEngine:
        return ScreenerEngine()

    @pytest.mark.asyncio
    async def test_screen_not_implemented(self, engine: ScreenerEngine):
        query = ScreenerQuery()
        with pytest.raises(NotImplementedError):
            await engine.screen(query)

    @pytest.mark.asyncio
    async def test_get_available_fields_not_implemented(self, engine: ScreenerEngine):
        with pytest.raises(NotImplementedError):
            await engine.get_available_fields()
