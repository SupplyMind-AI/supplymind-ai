from pathlib import Path
from fastapi import APIRouter, Depends
from sqlalchemy import text
from apps.api.dependencies import get_session, get_settings_dependency

router=APIRouter(prefix="/health",tags=["health"])

@router.get("")
async def health(session=Depends(get_session), cfg=Depends(get_settings_dependency)):
    services={}
    try:
        await session.execute(text("SELECT 1"));services["postgresql"]={"status":"connected"}
    except Exception as exc:
        services["postgresql"]={"status":"error","detail":str(exc)}
    d=Path(cfg.champion_model_directory)
    services["champion_model"]={"status":"loaded" if (d/"model.joblib").exists() and (d/"metadata.json").exists() else "missing"}
    services["openai"]={"status":"configured" if cfg.openai_api_key else "missing"}
    services["pinecone"]={"status":"configured" if cfg.pinecone_api_key and cfg.pinecone_index_host else "missing"}
    services["open_meteo"]={"status":"configured"}
    services["gdelt"]={"status":"configured"}
    services["langsmith"]={"status":"enabled" if cfg.langsmith_tracing and cfg.langsmith_api_key else "disabled"}
    overall="ok" if services["postgresql"]["status"]=="connected" and services["champion_model"]["status"]=="loaded" else "degraded"
    return {"status":overall,"services":services}
