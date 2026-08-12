"""Application configuration loaded from environment variables."""
from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    environment: str = 'development'
    api_host: str = '127.0.0.1'
    api_port: int = 8000
    cors_origins: str = 'http://localhost:5173'
    database_url: str = 'postgresql+asyncpg://supplymind:supplymind@localhost:5432/supplymind'
    database_echo: bool = False
    database_pool_size: int = 5
    database_max_overflow: int = 10
    champion_model_directory: Path = Path('models/champion')
    open_meteo_forecast_url: str = 'https://api.open-meteo.com/v1/forecast'
    open_meteo_geocoding_url: str = 'https://geocoding-api.open-meteo.com/v1/search'
    weather_forecast_days: int = 7
    gdelt_doc_url: str = 'https://api.gdeltproject.org/api/v2/doc/doc'
    gdelt_query: str = '("supply chain" OR logistics OR shipping OR port OR strike OR disruption OR flood OR wildfire OR storm)'
    gdelt_timespan: str = '24h'
    gdelt_max_records: int = 75
    openai_api_key: str | None = None
    llm_model: str = 'gpt-5-mini'
    embedding_model: str = 'text-embedding-3-small'
    pinecone_api_key: str | None = None
    pinecone_index_host: str | None = None
    pinecone_index_name: str = 'supplymind-knowledge'
    pinecone_cloud: str = 'aws'
    pinecone_region: str = 'us-east-1'
    embedding_dimension: int = 1536
    pinecone_namespace_documents: str = 'enterprise-documents'
    pinecone_namespace_events: str = 'supply-chain-events'
    semantic_search_top_k: int = 5
    enterprise_documents_directory: Path = Path('data/enterprise_documents')
    document_chunk_size: int = 1200
    document_chunk_overlap: int = 180
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = 'supplymind-ai'
    retraining_min_samples: int = 500
    retraining_max_psi: float = 0.20
    retraining_min_f1: float = 0.65
    @property
    def parsed_cors_origins(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(',') if x.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
