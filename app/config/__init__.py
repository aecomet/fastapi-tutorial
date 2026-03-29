import os
from functools import lru_cache

from app.config.base import Settings


@lru_cache
def get_settings() -> Settings:
    """APP_ENV 環境変数に応じた Settings インスタンスを返す（キャッシュ済み）。"""
    env = os.getenv("APP_ENV", "local")
    if env == "production":
        from app.config.production import ProductionSettings

        return ProductionSettings()
    from app.config.local import LocalSettings

    return LocalSettings()
