from enum import StrEnum

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["health"])

# アプリ起動完了フラグ（startup probe 用）
_startup_complete = False


def set_startup_complete() -> None:
    global _startup_complete
    _startup_complete = True


class HealthStatus(StrEnum):
    ok = "ok"
    degraded = "degraded"


class HealthResponse(BaseModel):
    status: HealthStatus
    detail: str


@router.get(
    "/startup",
    response_model=HealthResponse,
    summary="Startup probe",
    description="アプリケーションの起動完了を確認する。起動完了前は 503 を返す。",
)
def startup_probe() -> HealthResponse:
    """K8s startupProbe 用エンドポイント。"""
    if not _startup_complete:
        from fastapi import HTTPException

        raise HTTPException(status_code=503, detail="Application is still starting up")
    return HealthResponse(status=HealthStatus.ok, detail="Application startup complete")


@router.get(
    "/readiness",
    response_model=HealthResponse,
    summary="Readiness probe",
    description="アプリケーションがトラフィックを受け付けられる状態かを確認する。",
)
def readiness_probe() -> HealthResponse:
    """K8s readinessProbe 用エンドポイント。"""
    return HealthResponse(status=HealthStatus.ok, detail="Application is ready")


@router.get(
    "/liveness",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="アプリケーションが生存しているかを確認する。",
)
def liveness_probe() -> HealthResponse:
    """K8s livenessProbe 用エンドポイント。"""
    return HealthResponse(status=HealthStatus.ok, detail="Application is alive")
