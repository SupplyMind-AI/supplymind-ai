from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: str = "development"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173"

    database_url: str = (
        "postgresql+asyncpg://supplymind:supplymind@localhost:5432/supplymind"
    )
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10

    champion_model_directory: Path = Path("models/champion")

    open_meteo_forecast_url: str = "https://api.open-meteo.com/v1/forecast"
    open_meteo_geocoding_url: str = "https://geocoding-api.open-meteo.com/v1/search"
    weather_forecast_days: int = 7

    # NewsAPI.ai / Event Registry. Kept server-side only.
    news_api_ai_api_key: str | None = None
    news_api_ai_url: str = "https://eventregistry.org/api/v1/article/getArticles"
    news_api_ai_query: str = (
        "port congestion OR port closure OR shipping disruption OR "
        "freight disruption OR cargo disruption OR logistics disruption OR "
        "supply chain disruption OR border closure OR rail disruption OR "
        "transport strike OR port strike OR blockade OR flooding OR typhoon OR wildfire"
    )
    news_api_ai_language: str = "eng"
    news_api_ai_lookback_days: int = 3
    news_api_ai_max_records: int = 40
    news_api_ai_timeout_seconds: float = 20.0
    news_api_ai_max_retries: int = 3
    news_api_ai_retry_wait_seconds: float = 2.0

    # Deprecated GDELT settings retained only so old modules remain import-compatible.
    gdelt_doc_url: str = "https://api.gdeltproject.org/api/v2/doc/doc"
    gdelt_query: str = ""
    gdelt_timespan: str = "24h"
    gdelt_max_records: int = 50

    openai_api_key: str | None = None
    llm_model: str = "gpt-5.6"
    embedding_model: str = "text-embedding-3-small"

    pinecone_api_key: str | None = None
    pinecone_index_host: str | None = None
    pinecone_index_name: str = "supplymind-knowledge"
    pinecone_cloud: str = "aws"
    pinecone_region: str = "us-east-1"
    embedding_dimension: int = 1536
    pinecone_namespace_documents: str = "enterprise-documents"
    pinecone_namespace_events: str = "supply-chain-events"
    semantic_search_top_k: int = 5

    enterprise_documents_directory: Path = Path("data/enterprise_documents")
    document_chunk_size: int = 1200
    document_chunk_overlap: int = 180

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "supplymind-ai"

    retraining_min_samples: int = 500
    retraining_max_psi: float = 0.20
    retraining_min_f1: float = 0.65

    @property
    def parsed_cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
