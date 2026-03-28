from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root_returns_hello_world():
    """GET / が Hello World を返すこと"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_read_root_content_type_is_json():
    """GET / のレスポンスが JSON であること"""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"
