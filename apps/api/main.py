"""SupplyMind FastAPI application."""
from __future__ import annotations
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.routers import alerts, assistant, dashboard, events, health, monitoring, predictions, retraining, search, settings, shipments, weather
from supplymind.features.model_registry.application.bootstrap import register_champion_if_available
from supplymind.features.model_registry.infrastructure.repositories import SqlAlchemyModelRegistryRepository
from supplymind.shared.config.settings import get_settings
from supplymind.shared.infrastructure.database.session import dispose_engine, session_scope

cfg=get_settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    if cfg.langsmith_tracing:
        os.environ["LANGSMITH_TRACING"]="true";os.environ["LANGSMITH_PROJECT"]=cfg.langsmith_project
        if cfg.langsmith_api_key:os.environ["LANGSMITH_API_KEY"]=cfg.langsmith_api_key
    try:
        async with session_scope() as session:
            await register_champion_if_available(registry=SqlAlchemyModelRegistryRepository(session),model_directory=cfg.champion_model_directory)
    except Exception as exc:
        print(f"Champion bootstrap warning: {exc}")
    yield
    await dispose_engine()

app=FastAPI(title="SupplyMind AI",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=cfg.parsed_cors_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.get("/health")
async def root_health():return {"status":"ok","service":"SupplyMind AI"}

for router in (dashboard.router,assistant.router,shipments.router,predictions.router,alerts.router,events.router,weather.router,search.router,retraining.router,monitoring.router,settings.router,health.router):
    app.include_router(router,prefix="/api")
