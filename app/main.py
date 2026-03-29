import json
import logging
import logging.config
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.config import get_settings
from app.middleware import RequestLoggingMiddleware
from app.presentation.routers import authors, books, health, root
from app.presentation.routers.health import set_startup_complete

# APP_ENV に応じたログ設定を適用（uvicorn のログ設定より後に実行されるため上書き可能）
_settings = get_settings()
_log_config_path = Path(__file__).parent / "config" / f"log_config.{_settings.app_env}.json"
if not _log_config_path.exists():
    _log_config_path = Path(__file__).parent / "config" / "log_config.local.json"
with _log_config_path.open() as _f:
    logging.config.dictConfig(json.load(_f))

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    import app.infrastructure.models  # noqa: F401 — Base.metadata にモデルを登録
    from app.infrastructure.database import Base, engine

    Base.metadata.create_all(bind=engine)
    set_startup_complete()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

app.include_router(root.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(authors.router, prefix="/api/v2")
app.include_router(books.router, prefix="/api/v2")
