"""FastAPI dependency wiring at the infrastructure boundary."""

from __future__ import annotations

from collections.abc import AsyncIterator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.events.infrastructure.repositories import (
    SqlAlchemyEventRepository,
)
from supplymind.features.external_intelligence.application.weather import GetWeatherRisk
from supplymind.features.external_intelligence.infrastructure.gdelt import GdeltClient
from supplymind.features.external_intelligence.infrastructure.open_meteo import (
    OpenMeteoClient,
)
from supplymind.features.knowledge.application.search import SemanticSearch
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


async def get_session() -> AsyncIterator[AsyncSession]:
    """One transaction-scoped SQLAlchemy session per request."""

    async with AsyncSessionFactory() as session:
        async with session.begin():
            yield session


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
def get_gdelt_client() -> GdeltClient:
    settings = get_settings()
    return GdeltClient(
        base_url=settings.gdelt_doc_url,
        query=settings.gdelt_query,
        timespan=settings.gdelt_timespan,
        max_records=settings.gdelt_max_records,
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


@lru_cache
def get_champion_runtime() -> ChampionModelRuntime:
    return ChampionModelRuntime(get_settings().champion_model_directory)
