"""Application configuration loaded from environment variables."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# -------------------
# Settings
# -------------------

class Settings(BaseSettings):
    """Runtime settings shared by API, migrations, workers, and scripts."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"

    database_url: str = (
        "postgresql+asyncpg://supplymind:supplymind@localhost:5432/supplymind"
    )

    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10


# -------------------
# Cached settings
# -------------------

@lru_cache
def get_settings() -> Settings:
    """Return one cached Settings instance per process."""

    return Settings()
