"""Tests for screener router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.screener.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestScreenerRouter:
    def test_screen_endpoint_exists(self, client: TestClient):
        response = client.post("/screener/screen", json={"filters": []})
        assert response.status_code == 501

    def test_get_fields_endpoint_exists(self, client: TestClient):
        response = client.get("/screener/fields")
        assert response.status_code == 501
