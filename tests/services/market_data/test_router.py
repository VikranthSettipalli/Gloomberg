"""Tests for market data router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.market_data.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestMarketDataRouter:
    def test_get_quote_endpoint_exists(self, client: TestClient):
        """GET /market/quote/{symbol} endpoint exists."""
        response = client.get("/market/quote/RELIANCE.NS")
        # Should return 501 (not implemented) not 404
        assert response.status_code == 501

    def test_get_history_endpoint_exists(self, client: TestClient):
        """GET /market/history/{symbol} endpoint exists."""
        response = client.get(
            "/market/history/RELIANCE.NS",
            params={"start": "2026-01-01", "end": "2026-03-01"},
        )
        assert response.status_code == 501

    def test_get_history_requires_dates(self, client: TestClient):
        """History endpoint requires start and end dates."""
        response = client.get("/market/history/RELIANCE.NS")
        assert response.status_code == 422  # Validation error

    def test_invalid_interval_rejected(self, client: TestClient):
        """Invalid interval values are rejected."""
        response = client.get(
            "/market/history/RELIANCE.NS",
            params={"start": "2026-01-01", "end": "2026-03-01", "interval": "invalid"},
        )
        assert response.status_code == 422
