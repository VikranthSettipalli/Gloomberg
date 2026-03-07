"""Tests for gateway main application."""
import pytest
from fastapi.testclient import TestClient

from gateway.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class TestGateway:
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_root_returns_endpoints(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "market_data" in data["endpoints"]

    def test_timing_header(self, client: TestClient):
        response = client.get("/health")
        assert "x-response-time" in response.headers

    def test_market_router_mounted(self, client: TestClient):
        response = client.get("/market/quote/TEST")
        assert response.status_code in [200, 501]  # Not 404

    def test_fundamentals_router_mounted(self, client: TestClient):
        response = client.get("/fundamentals/ratios/TEST")
        assert response.status_code in [200, 501]

    def test_index_router_mounted(self, client: TestClient):
        response = client.get("/indices/NIFTY50")
        assert response.status_code in [200, 501]

    def test_estimates_router_mounted(self, client: TestClient):
        response = client.get("/estimates/TEST")
        assert response.status_code in [200, 501]

    def test_shareholding_router_mounted(self, client: TestClient):
        response = client.get("/shareholding/TEST")
        assert response.status_code in [200, 501]

    def test_screener_router_mounted(self, client: TestClient):
        response = client.get("/screener/fields")
        assert response.status_code in [200, 501]
