from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Query
from apps.api.dependencies import get_event_repository, get_gdelt_client, get_open_meteo_client, get_settings_dependency
from supplymind.features.events.application.use_cases import UpsertEvent
from supplymind.features.external_intelligence.infrastructure.event_extractor import StructuredEventExtractor
from supplymind.features.external_intelligence.application.gdelt_ingestion import IngestGdeltEvents

router=APIRouter(prefix="/events",tags=["events"])

@router.get("")
async def list_items(limit:int=Query(100,ge=1,le=200), event_type:str|None=None, country:str|None=None, min_severity:float|None=Query(None,ge=0,le=1), repo=Depends(get_event_repository)):
    rows=await repo.list_active(at=datetime.now(timezone.utc),limit=limit)
    result=[]
    for e in rows:
        if event_type and e.event_type != event_type: continue
        if country and (e.country or "").casefold()!=country.casefold(): continue
        if min_severity is not None and (e.severity or 0)<min_severity: continue
        result.append({"id":str(e.id),"source":e.source,"event_type":e.event_type,"title":e.title,"description":e.description,"severity":e.severity,"country":e.country,"region":e.region,"latitude":e.latitude,"longitude":e.longitude,"starts_at":e.starts_at.isoformat() if e.starts_at else None,"created_at":e.created_at.isoformat() if e.created_at else None})
    return result

@router.post("/refresh")
async def refresh(repo=Depends(get_event_repository),cfg=Depends(get_settings_dependency)):
    use=IngestGdeltEvents(gdelt_client=get_gdelt_client(),extractor=StructuredEventExtractor(model=cfg.llm_model,api_key=cfg.openai_api_key),geocoder=get_open_meteo_client(),upsert_event=UpsertEvent(repo))
    return {"ingested":len(await use.execute())}
