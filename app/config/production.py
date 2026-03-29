from app.config.base import Settings


class ProductionSettings(Settings):
    app_env: str = "production"
    log_level: str = "INFO"
