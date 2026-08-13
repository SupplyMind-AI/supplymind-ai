from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from apps.api.dependencies import get_event_repository, get_prediction_repository, get_shipment_repository

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("")
async def alerts(predictions=Depends(get_prediction_repository), shipments=Depends(get_shipment_repository), events=Depends(get_event_repository)):
    items=[]
    for p in await predictions.list_recent(limit=100):
        if p.risk_level not in {"high", "medium"}: continue
        s=await shipments.get(p.shipment_id)
        items.append({"id":f"prediction:{p.id}","kind":"prediction","severity":p.risk_level,"title":f"{s.external_id if s else p.shipment_id} predicted delayed","detail":f"Delay score {p.delay_probability:.1%} vs threshold {p.threshold:.1%}","created_at":p.created_at.isoformat() if p.created_at else None})
    for e in await events.list_active(at=datetime.now(timezone.utc), limit=100):
        if (e.severity or 0) < 0.7: continue
        items.append({"id":f"event:{e.id}","kind":"event","severity":"high" if (e.severity or 0)>=0.8 else "medium","title":e.title,"detail":f"{e.event_type} · {e.country or 'Unknown'} · severity {(e.severity or 0):.2f}","created_at":e.created_at.isoformat() if e.created_at else None})
    return sorted(items, key=lambda x: x.get("created_at") or "", reverse=True)[:50]
