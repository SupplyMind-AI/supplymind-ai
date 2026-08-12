from datetime import datetime,timezone
from fastapi import APIRouter,Depends
from apps.api.dependencies import get_event_repository, get_gdelt_client, get_open_meteo_client, get_settings_dependency
from supplymind.features.events.application.use_cases import UpsertEvent
from supplymind.features.external_intelligence.infrastructure.event_extractor import StructuredEventExtractor
from supplymind.features.external_intelligence.application.gdelt_ingestion import IngestGdeltEvents
router=APIRouter(prefix='/events',tags=['events'])
@router.get('')
async def list_items(limit:int=100,repo=Depends(get_event_repository)):return [x.__dict__ for x in await repo.list_active(at=datetime.now(timezone.utc),limit=min(max(limit,1),200))]
@router.post('/refresh')
async def refresh(repo=Depends(get_event_repository),cfg=Depends(get_settings_dependency)):
 use=IngestGdeltEvents(gdelt_client=get_gdelt_client(),extractor=StructuredEventExtractor(model=cfg.llm_model,api_key=cfg.openai_api_key),geocoder=get_open_meteo_client(),upsert_event=UpsertEvent(repo));return {'ingested':len(await use.execute())}
