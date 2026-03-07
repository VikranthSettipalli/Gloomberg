"""Tests for EstimatesProvider base class."""
import pytest
from abc import ABC

from services.estimates.providers.base import EstimatesProvider


class TestEstimatesProviderInterface:
    def test_is_abstract(self):
        assert issubclass(EstimatesProvider, ABC)

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            EstimatesProvider()  # type: ignore

    def test_has_required_methods(self):
        methods = ["get_estimates", "get_price_targets", "get_recommendations"]
        for method in methods:
            assert hasattr(EstimatesProvider, method)
