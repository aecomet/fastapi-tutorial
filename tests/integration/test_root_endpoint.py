import fakeredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.infrastructure.models  # noqa: F401
from app.infrastructure.database import Base, get_db
from app.infrastructure.redis import get_redis
from app.main import app

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


def override_get_redis():
    client = fakeredis.FakeRedis(decode_responses=True)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


def test_read_root_returns_hello_world(client: TestClient):
    """GET /api/v1/ が Hello World メッセージとルート一覧を返すこと"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Hello World"
    assert isinstance(body["routes"], list)
    assert len(body["routes"]) > 0


def test_read_root_contains_health_routes(client: TestClient):
    """GET /api/v1/ のルート一覧にヘルスチェックエンドポイントが含まれること"""
    response = client.get("/api/v1/")
    paths = [r["path"] for r in response.json()["routes"]]
    assert "/api/v1/health/startup" in paths
    assert "/api/v1/health/readiness" in paths
    assert "/api/v1/health/liveness" in paths


def test_read_root_content_type_is_json(client: TestClient):
    """GET /api/v1/ のレスポンスが JSON であること"""
    response = client.get("/api/v1/")
    assert response.headers["content-type"] == "application/json"


def test_liveness_probe(client: TestClient):
    """GET /api/v1/health/liveness が 200 を返すこと"""
    response = client.get("/api/v1/health/liveness")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_probe(client: TestClient):
    """GET /api/v1/health/readiness が 200 を返すこと"""
    response = client.get("/api/v1/health/readiness")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_startup_probe(client: TestClient):
    """GET /api/v1/health/startup が lifespan 起動完了後に 200 を返すこと"""
    response = client.get("/api/v1/health/startup")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["checks"]["database"] == "ok"
    assert body["checks"]["redis"] == "ok"
