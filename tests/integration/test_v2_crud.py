import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.infrastructure.models  # noqa: F401 — Base.metadata にモデルを登録
from app.infrastructure.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite://"  # インメモリ SQLite

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # 全接続で同一 DB を共有
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=test_engine)
    app.dependency_overrides.clear()


# ── Author CRUD ──────────────────────────────────────────────────────────────


def test_create_author(client: TestClient):
    """POST /api/v2/authors で著者を登録できること"""
    res = client.post("/api/v2/authors/", json={"name": "夏目漱石", "bio": "明治の文豪"})
    assert res.status_code == 201
    body = res.json()
    assert body["name"] == "夏目漱石"
    assert body["id"] is not None


def test_list_authors(client: TestClient):
    """GET /api/v2/authors で著者一覧を取得できること"""
    client.post("/api/v2/authors/", json={"name": "芥川龍之介"})
    res = client.get("/api/v2/authors/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_get_author(client: TestClient):
    """GET /api/v2/authors/{id} で著者を取得できること"""
    created = client.post("/api/v2/authors/", json={"name": "太宰治"}).json()
    res = client.get(f"/api/v2/authors/{created['id']}")
    assert res.status_code == 200
    assert res.json()["name"] == "太宰治"


def test_get_author_not_found(client: TestClient):
    """存在しない著者は 404 を返すこと"""
    res = client.get("/api/v2/authors/999")
    assert res.status_code == 404


def test_update_author(client: TestClient):
    """PUT /api/v2/authors/{id} で著者を更新できること"""
    created = client.post("/api/v2/authors/", json={"name": "川端康成"}).json()
    res = client.put(f"/api/v2/authors/{created['id']}", json={"bio": "ノーベル文学賞受賞者"})
    assert res.status_code == 200
    assert res.json()["bio"] == "ノーベル文学賞受賞者"


def test_delete_author(client: TestClient):
    """DELETE /api/v2/authors/{id} で著者を削除できること"""
    created = client.post("/api/v2/authors/", json={"name": "三島由紀夫"}).json()
    res = client.delete(f"/api/v2/authors/{created['id']}")
    assert res.status_code == 204
    assert client.get(f"/api/v2/authors/{created['id']}").status_code == 404


# ── Book CRUD ─────────────────────────────────────────────────────────────────


def _create_author(client: TestClient, name: str = "テスト著者") -> dict:
    return client.post("/api/v2/authors/", json={"name": name}).json()


def test_create_book(client: TestClient):
    """POST /api/v2/books で書籍を登録できること"""
    author = _create_author(client)
    res = client.post(
        "/api/v2/books/",
        json={
            "title": "吾輩は猫である",
            "isbn": "978-4-10-101001-7",
            "published_year": 1905,
            "genre": "小説",
            "author_id": author["id"],
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "吾輩は猫である"
    assert body["author_id"] == author["id"]


def test_create_book_invalid_author(client: TestClient):
    """存在しない author_id で書籍登録すると 404 を返すこと"""
    res = client.post("/api/v2/books/", json={"title": "仮の本", "author_id": 999})
    assert res.status_code == 404


def test_list_books(client: TestClient):
    """GET /api/v2/books で書籍一覧を取得できること"""
    author = _create_author(client)
    client.post("/api/v2/books/", json={"title": "坊っちゃん", "author_id": author["id"]})
    res = client.get("/api/v2/books/")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_list_books_filter_by_author(client: TestClient):
    """GET /api/v2/books?author_id=X で著者で絞り込みできること"""
    a1 = _create_author(client, "著者A")
    a2 = _create_author(client, "著者B")
    client.post("/api/v2/books/", json={"title": "本A", "author_id": a1["id"]})
    client.post("/api/v2/books/", json={"title": "本B", "author_id": a2["id"]})
    res = client.get(f"/api/v2/books/?author_id={a1['id']}")
    assert res.status_code == 200
    assert all(b["author_id"] == a1["id"] for b in res.json())


def test_update_book(client: TestClient):
    """PUT /api/v2/books/{id} で書籍を更新できること"""
    author = _create_author(client)
    book = client.post(
        "/api/v2/books/", json={"title": "旧タイトル", "author_id": author["id"]}
    ).json()
    res = client.put(f"/api/v2/books/{book['id']}", json={"title": "新タイトル"})
    assert res.status_code == 200
    assert res.json()["title"] == "新タイトル"


def test_delete_book(client: TestClient):
    """DELETE /api/v2/books/{id} で書籍を削除できること"""
    author = _create_author(client)
    book = client.post("/api/v2/books/", json={"title": "削除本", "author_id": author["id"]}).json()
    res = client.delete(f"/api/v2/books/{book['id']}")
    assert res.status_code == 204
    assert client.get(f"/api/v2/books/{book['id']}").status_code == 404
