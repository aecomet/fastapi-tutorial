from enum import StrEnum

import redis as redis_lib
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.infrastructure.database import get_db
from app.infrastructure.redis import get_redis

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
    checks: dict[str, HealthStatus] | None = None


def _check_database(db: Session) -> HealthStatus:
    try:
        db.execute(text("SELECT 1"))
        return HealthStatus.ok
    except Exception:
        return HealthStatus.degraded


def _check_redis(client: redis_lib.Redis) -> HealthStatus:
    try:
        client.ping()
        return HealthStatus.ok
    except Exception:
        return HealthStatus.degraded


@router.get(
    "/startup",
    response_model=HealthResponse,
    summary="Startup probe",
    description="アプリケーションの起動完了と各ミドルウェアの疎通を確認する。",
)
def startup_probe(
    db: Session = Depends(get_db),
    redis_client: redis_lib.Redis = Depends(get_redis),
) -> HealthResponse:
    """K8s startupProbe 用エンドポイント。DB・Redis の疎通チェックを含む。"""
    if not _startup_complete:
        raise HTTPException(status_code=503, detail="Application is still starting up")

    checks = {
        "database": _check_database(db),
        "redis": _check_redis(redis_client),
    }
    all_ok = all(v == HealthStatus.ok for v in checks.values())
    overall = HealthStatus.ok if all_ok else HealthStatus.degraded
    if overall != HealthStatus.ok:
        raise HTTPException(
            status_code=503,
            detail=HealthResponse(
                status=overall,
                detail="One or more middleware checks failed",
                checks=checks,
            ).model_dump(),
        )
    return HealthResponse(
        status=HealthStatus.ok,
        detail="Application startup complete",
        checks=checks,
    )


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
