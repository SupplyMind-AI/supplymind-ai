from fastapi import APIRouter,Depends
from apps.api.dependencies import get_shipment_repository, get_prediction_repository, get_event_repository, get_weather_service, get_semantic_search, get_settings_dependency
from supplymind.features.assistant.application.tools import build_assistant_tools
from supplymind.features.assistant.application.graph import SupplyMindAssistant
from supplymind.features.assistant.domain.schemas import AssistantRequest
router=APIRouter(prefix='/assistant',tags=['assistant'])
@router.post('')
async def ask(req:AssistantRequest,sr=Depends(get_shipment_repository),pr=Depends(get_prediction_repository),er=Depends(get_event_repository),ws=Depends(get_weather_service),ss=Depends(get_semantic_search),cfg=Depends(get_settings_dependency)):
 tools=build_assistant_tools(shipment_repository=sr,prediction_repository=pr,event_repository=er,weather_service=ws,semantic_search=ss);return await SupplyMindAssistant(tools=tools,model=cfg.llm_model,api_key=cfg.openai_api_key).ask(req)
