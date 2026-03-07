"""Tests for fundamentals router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.fundamentals.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestFundamentalsRouter:
    def test_get_financials_endpoint_exists(self, client: TestClient):
        response = client.get("/fundamentals/financials/RELIANCE")
        assert response.status_code == 501

    def test_get_ratios_endpoint_exists(self, client: TestClient):
        response = client.get("/fundamentals/ratios/RELIANCE")
        assert response.status_code == 501

    def test_get_filings_endpoint_exists(self, client: TestClient):
        response = client.get("/fundamentals/filings/RELIANCE")
        assert response.status_code == 501

    def test_invalid_period_rejected(self, client: TestClient):
        response = client.get("/fundamentals/financials/RELIANCE?period=invalid")
        assert response.status_code == 422
