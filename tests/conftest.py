"""Shared pytest fixtures."""
import pytest
from datetime import datetime, date
from decimal import Decimal


@pytest.fixture
def sample_symbol() -> str:
    return "RELIANCE.NS"


@pytest.fixture
def sample_timestamp() -> datetime:
    return datetime(2026, 3, 8, 10, 30, 0)


@pytest.fixture
def sample_date() -> date:
    return date(2026, 3, 8)


@pytest.fixture
def sample_price() -> Decimal:
    return Decimal("2500.50")
