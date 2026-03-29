import fakeredis
import fakeredis.aioredis
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.infrastructure.models  # noqa: F401
from app.infrastructure.database import Base, get_db
from app.infrastructure.redis import get_async_redis, get_redis
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


async def override_get_async_redis():
    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_async_redis] = override_get_async_redis
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


def test_publish_event_returns_event_response(client: TestClient):
    """POST /api/v3/dpar/{channel}/publish がイベントを返すこと"""
    response = client.post(
        "/api/v3/dpar/test-channel/publish",
        json={"payload": {"key": "value", "count": 42}},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["channel"] == "test-channel"
    assert body["payload"] == {"key": "value", "count": 42}
    assert "event_id" in body
    assert "timestamp" in body


def test_publish_event_assigns_unique_event_ids(client: TestClient):
    """連続して Publish したイベントがそれぞれ異なる event_id を持つこと"""
    r1 = client.post("/api/v3/dpar/ch/publish", json={"payload": {"x": 1}})
    r2 = client.post("/api/v3/dpar/ch/publish", json={"payload": {"x": 2}})
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["event_id"] != r2.json()["event_id"]


def test_publish_event_different_channels(client: TestClient):
    """異なるチャンネルに Publish できること"""
    r1 = client.post("/api/v3/dpar/channel-a/publish", json={"payload": {"msg": "a"}})
    r2 = client.post("/api/v3/dpar/channel-b/publish", json={"payload": {"msg": "b"}})
    assert r1.status_code == 200
    assert r1.json()["channel"] == "channel-a"
    assert r2.status_code == 200
    assert r2.json()["channel"] == "channel-b"
