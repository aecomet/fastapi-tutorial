from app.services.root import ROUTES, RootResponse, build_root_response


def test_build_root_response_message():
    """build_root_response が 'Hello World' メッセージを返すこと"""
    result = build_root_response()
    assert isinstance(result, RootResponse)
    assert result.message == "Hello World"


def test_build_root_response_has_routes():
    """build_root_response がルート一覧を含むこと"""
    result = build_root_response()
    assert len(result.routes) > 0


def test_routes_include_health_endpoints():
    """ROUTES にヘルスチェックエンドポイントが含まれること"""
    paths = [r.path for r in ROUTES]
    assert "/health/startup" in paths
    assert "/health/readiness" in paths
    assert "/health/liveness" in paths


def test_routes_include_docs():
    """ROUTES に Swagger UI へのリンクが含まれること"""
    paths = [r.path for r in ROUTES]
    assert "/docs" in paths
