"""Tests for IndexProvider base class."""
import pytest
from abc import ABC

from services.index.providers.base import IndexProvider


class TestIndexProviderInterface:
    def test_is_abstract(self):
        assert issubclass(IndexProvider, ABC)

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            IndexProvider()  # type: ignore

    def test_has_required_methods(self):
        methods = ["get_index", "get_constituents"]
        for method in methods:
            assert hasattr(IndexProvider, method)
