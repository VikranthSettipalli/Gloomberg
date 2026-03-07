"""Tests for index router."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.index.router import router


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


class TestIndexRouter:
    def test_get_index_endpoint_exists(self, client: TestClient):
        response = client.get("/indices/NIFTY50")
        assert response.status_code == 501

    def test_get_constituents_endpoint_exists(self, client: TestClient):
        response = client.get("/indices/NIFTY50/constituents")
        assert response.status_code == 501
