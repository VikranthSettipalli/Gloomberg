"""Tests for estimates router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.estimates.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestEstimatesRouter:
    def test_get_estimates_endpoint_exists(self, client: TestClient):
        response = client.get("/estimates/AAPL")
        assert response.status_code == 501

    def test_get_price_targets_endpoint_exists(self, client: TestClient):
        response = client.get("/estimates/AAPL/price-targets")
        assert response.status_code == 501

    def test_get_recommendations_endpoint_exists(self, client: TestClient):
        response = client.get("/estimates/AAPL/recommendations")
        assert response.status_code == 501
