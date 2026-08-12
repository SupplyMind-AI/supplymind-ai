"""SupplyMind FastAPI application."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from apps.api.routers import assistant, dashboard, events, monitoring, predictions, retraining, search, settings, shipments
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.routers import (
    weather,
)
from supplymind.shared.config.settings import get_settings
from supplymind.shared.infrastructure.database.session import dispose_engine

settings_config = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configure tracing before traffic and dispose DB pools on shutdown."""

    if settings_config.langsmith_tracing:
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = settings_config.langsmith_project
        if settings_config.langsmith_api_key:
            os.environ["LANGSMITH_API_KEY"] = settings_config.langsmith_api_key

    yield
    await dispose_engine()


app = FastAPI(
    title="SupplyMind AI",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings_config.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


for router in (
    dashboard.router,
    assistant.router,
    shipments.router,
    predictions.router,
    events.router,
    weather.router,
    search.router,
    retraining.router,
    monitoring.router,
    settings.router,
):
    app.include_router(router, prefix="/api")
