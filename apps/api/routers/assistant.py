import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from apps.api.dependencies import get_shipment_repository, get_prediction_repository, get_event_repository, get_weather_service, get_semantic_search, get_settings_dependency
from supplymind.features.assistant.application.tools import build_assistant_tools
from supplymind.features.assistant.application.graph import SupplyMindAssistant
from supplymind.features.assistant.application.streaming import SupplyMindStreamingAssistant
from supplymind.features.assistant.domain.schemas import AssistantRequest

router=APIRouter(prefix="/assistant",tags=["assistant"])

def _tools(sr, pr, er, ws, ss):
    return build_assistant_tools(shipment_repository=sr,prediction_repository=pr,event_repository=er,weather_service=ws,semantic_search=ss)

@router.post("")
async def ask(req: AssistantRequest, sr=Depends(get_shipment_repository), pr=Depends(get_prediction_repository), er=Depends(get_event_repository), ws=Depends(get_weather_service), ss=Depends(get_semantic_search), cfg=Depends(get_settings_dependency)):
    return await SupplyMindAssistant(tools=_tools(sr,pr,er,ws,ss),model=cfg.llm_model,api_key=cfg.openai_api_key).ask(req)

@router.post("/stream")
async def ask_stream(req: AssistantRequest, sr=Depends(get_shipment_repository), pr=Depends(get_prediction_repository), er=Depends(get_event_repository), ws=Depends(get_weather_service), ss=Depends(get_semantic_search), cfg=Depends(get_settings_dependency)):
    assistant=SupplyMindStreamingAssistant(tools=_tools(sr,pr,er,ws,ss),model=cfg.llm_model,api_key=cfg.openai_api_key)
    async def generate():
        async for event in assistant.stream(req):
            yield f"data: {json.dumps(event, default=str)}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream", headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})
