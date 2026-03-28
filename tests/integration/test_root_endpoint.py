import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_read_root_returns_hello_world(client: TestClient):
    """GET / が Hello World を返すこと"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_root_content_type_is_json(client: TestClient):
    """GET / のレスポンスが JSON であること"""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"


def test_liveness_probe(client: TestClient):
    """GET /health/liveness が 200 を返すこと"""
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_probe(client: TestClient):
    """GET /health/readiness が 200 を返すこと"""
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_startup_probe(client: TestClient):
    """GET /health/startup が lifespan 起動完了後に 200 を返すこと"""
    response = client.get("/health/startup")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
