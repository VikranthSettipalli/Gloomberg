"""Tests for shareholding router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.shareholding.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestShareholdingRouter:
    def test_get_shareholding_endpoint_exists(self, client: TestClient):
        response = client.get("/shareholding/RELIANCE")
        assert response.status_code == 501

    def test_get_shareholding_history_endpoint_exists(self, client: TestClient):
        response = client.get("/shareholding/RELIANCE/history")
        assert response.status_code == 501
