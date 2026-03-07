"""Tests for MarketDataProvider base class."""
import pytest
from abc import ABC

from services.market_data.providers.base import MarketDataProvider


class TestMarketDataProviderInterface:
    def test_is_abstract(self):
        """MarketDataProvider should be an abstract class."""
        assert issubclass(MarketDataProvider, ABC)

    def test_cannot_instantiate(self):
        """Cannot instantiate abstract class directly."""
        with pytest.raises(TypeError):
            MarketDataProvider()  # type: ignore

    def test_has_required_methods(self):
        """Check required abstract methods exist."""
        methods = ["get_quote", "get_history", "stream_quotes"]
        for method in methods:
            assert hasattr(MarketDataProvider, method)
