from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "local"
    database_url: str = "sqlite:///./fastapi_dev.db"
    redis_url: str = "redis://localhost:6379/0"
    log_level: str = "INFO"
    dpar_worker_channel: str = "events"
