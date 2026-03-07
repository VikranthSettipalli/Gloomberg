"""Tests for FundamentalsProvider base class."""
import pytest
from abc import ABC

from services.fundamentals.providers.base import FundamentalsProvider


class TestFundamentalsProviderInterface:
    def test_is_abstract(self):
        assert issubclass(FundamentalsProvider, ABC)

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            FundamentalsProvider()  # type: ignore

    def test_has_required_methods(self):
        methods = ["get_financials", "get_ratios", "get_filings"]
        for method in methods:
            assert hasattr(FundamentalsProvider, method)
