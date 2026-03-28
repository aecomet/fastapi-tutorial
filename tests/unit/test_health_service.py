from app.routers.health import (
    HealthResponse,
    HealthStatus,
    liveness_probe,
    readiness_probe,
)


def test_liveness_returns_ok_status():
    """liveness_probe が status=ok を返すこと"""
    result = liveness_probe()
    assert isinstance(result, HealthResponse)
    assert result.status == HealthStatus.ok


def test_readiness_returns_ok_status():
    """readiness_probe が status=ok を返すこと"""
    result = readiness_probe()
    assert isinstance(result, HealthResponse)
    assert result.status == HealthStatus.ok


def test_health_response_has_detail():
    """HealthResponse に detail フィールドがあること"""
    r = HealthResponse(status=HealthStatus.ok, detail="alive")
    assert r.detail == "alive"
