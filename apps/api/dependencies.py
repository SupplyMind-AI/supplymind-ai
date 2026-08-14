"""FastAPI dependency wiring at the infrastructure boundary."""

from __future__ import annotations

from collections.abc import AsyncIterator
from functools import lru_cache

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.events.infrastructure.repositories import (
    SqlAlchemyEventRepository,
)
from supplymind.features.external_intelligence.application.weather import GetWeatherRisk
from supplymind.features.external_intelligence.infrastructure.news_api_ai import NewsApiAiClient
from supplymind.features.external_intelligence.infrastructure.open_meteo import (
    OpenMeteoClient,
)
from supplymind.features.knowledge.application.search import SemanticSearch
from supplymind.features.knowledge.application.rag import GroundedRag
from supplymind.features.knowledge.infrastructure.repositories import (
    SqlAlchemyDocumentRegistryRepository,
)
from supplymind.features.knowledge.infrastructure.vector_store import (
    PineconeSemanticStore,
)
from supplymind.features.model_registry.infrastructure.repositories import (
    SqlAlchemyModelRegistryRepository,
)
from supplymind.features.monitoring.infrastructure.repositories import (
    SqlAlchemyMonitoringRepository,
)
from supplymind.features.predictions.infrastructure.repositories import (
    SqlAlchemyPredictionRepository,
)
from supplymind.features.predictions.infrastructure.runtime import ChampionModelRuntime
from supplymind.features.retraining.infrastructure.repositories import (
    SqlAlchemyRetrainingRepository,
)
from supplymind.features.shipments.infrastructure.repositories import (
    SqlAlchemyShipmentRepository,
)
from supplymind.shared.config.settings import Settings, get_settings
from supplymind.shared.infrastructure.database.session import AsyncSessionFactory


from collections.abc import AsyncIterator

from fastapi import HTTPException
from sqlalchemy.exc import DBAPIError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncIterator[AsyncSession]:
    """Provide one SQLAlchemy session per request.

    SQLAlchemy 2.x automatically begins a transaction when the session
    executes its first database operation, so we must not combine an
    explicit connection check with `session.begin()`.
    """

    async with AsyncSessionFactory() as session:
        try:
            yield session

            # Commit writes performed during the request.
            if session.in_transaction():
                await session.commit()

        except (OperationalError, DBAPIError) as exc:
            if session.in_transaction():
                await session.rollback()

            raise HTTPException(
                status_code=503,
                detail="Database unavailable",
            ) from exc

        except Exception:
            if session.in_transaction():
                await session.rollback()

            # Important: preserve non-database exceptions so we can see
            # the real Assistant / LangGraph / Pinecone / OpenAI error.
            raise


def get_settings_dependency() -> Settings:
    return get_settings()


def get_shipment_repository(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyShipmentRepository(session)


def get_prediction_repository(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyPredictionRepository(session)


def get_event_repository(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyEventRepository(session)


def get_model_registry(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyModelRegistryRepository(session)


def get_monitoring_repository(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyMonitoringRepository(session)


def get_retraining_repository(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyRetrainingRepository(session)


def get_document_registry(session: AsyncSession = Depends(get_session)):
    return SqlAlchemyDocumentRegistryRepository(session)


@lru_cache
def get_open_meteo_client() -> OpenMeteoClient:
    settings = get_settings()
    return OpenMeteoClient(
        geocoding_url=settings.open_meteo_geocoding_url,
        forecast_url=settings.open_meteo_forecast_url,
        forecast_days=settings.weather_forecast_days,
    )


def get_weather_service() -> GetWeatherRisk:
    return GetWeatherRisk(get_open_meteo_client())


@lru_cache
def get_news_api_ai_client() -> NewsApiAiClient:
    settings = get_settings()
    return NewsApiAiClient(
        api_key=settings.news_api_ai_api_key,
        base_url=settings.news_api_ai_url,
        query=settings.news_api_ai_query,
        language=settings.news_api_ai_language,
        lookback_days=settings.news_api_ai_lookback_days,
        max_records=settings.news_api_ai_max_records,
        timeout_seconds=settings.news_api_ai_timeout_seconds,
        max_retries=settings.news_api_ai_max_retries,
        retry_wait_seconds=settings.news_api_ai_retry_wait_seconds,
    )


@lru_cache
def get_semantic_store() -> PineconeSemanticStore:
    settings = get_settings()
    if not settings.pinecone_api_key or not settings.pinecone_index_host:
        raise RuntimeError(
            "Semantic search requires PINECONE_API_KEY and "
            "PINECONE_INDEX_HOST."
        )

    return PineconeSemanticStore(
        pinecone_api_key=settings.pinecone_api_key,
        index_host=settings.pinecone_index_host,
        embedding_model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )


def get_semantic_search() -> SemanticSearch:
    settings = get_settings()
    return SemanticSearch(
        vector_store=get_semantic_store(),
        namespace=settings.pinecone_namespace_documents,
        default_top_k=settings.semantic_search_top_k,
    )


def get_rag_service() -> GroundedRag:
    settings = get_settings()
    return GroundedRag(
        semantic_search=get_semantic_search(),
        model=settings.llm_model,
        api_key=settings.openai_api_key,
    )


@lru_cache
def get_champion_runtime() -> ChampionModelRuntime:
    return ChampionModelRuntime(get_settings().champion_model_directory)
