"""Updated configuration with auth settings."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "SmartSkale LMS"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    version: str = "1.0.0"

    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/smartskale"

    # Security
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Logging
    log_level: str = "INFO"

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
