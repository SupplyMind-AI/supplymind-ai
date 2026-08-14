from fastapi import APIRouter, Depends

from apps.api.dependencies import get_settings_dependency

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
async def settings(cfg=Depends(get_settings_dependency)):
    return {
        "environment": cfg.environment,
        "llm_model": cfg.llm_model,
        "embedding_model": cfg.embedding_model,
        "semantic_search_enabled": bool(cfg.pinecone_api_key and cfg.pinecone_index_host),
        "langsmith_tracing": cfg.langsmith_tracing,
        "langsmith_project": cfg.langsmith_project,
        "champion_model_directory": str(cfg.champion_model_directory),
        "weather_forecast_days": cfg.weather_forecast_days,
        "news_api_ai": {"configured": bool(cfg.news_api_ai_api_key), "provider": "NewsAPI.ai"},
        "postgresql": {"configured": bool(cfg.database_url)},
        "pinecone": {"configured": bool(cfg.pinecone_api_key and cfg.pinecone_index_host)},
        "open_meteo": {"configured": True},
        "openai": {"configured": bool(cfg.openai_api_key)},
        "langsmith": {"configured": bool(cfg.langsmith_tracing and cfg.langsmith_api_key)},
        "retraining_policy": {
            "min_samples": cfg.retraining_min_samples,
            "max_psi": cfg.retraining_max_psi,
            "min_f1": cfg.retraining_min_f1,
        },
    }
