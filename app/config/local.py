from app.config.base import Settings


class LocalSettings(Settings):
    app_env: str = "local"
    database_url: str = "sqlite:///./fastapi_dev.db"
    log_level: str = "DEBUG"
