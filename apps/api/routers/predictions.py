from fastapi import APIRouter, Depends, HTTPException, Query
from apps.api.dependencies import get_champion_runtime, get_model_registry, get_prediction_repository, get_shipment_repository
from apps.api.schemas import PredictionRequest
from supplymind.features.predictions.application.predict import PredictShipment
from supplymind.features.predictions.application.persistence import RecordPrediction
from supplymind.features.predictions.domain.risk import decision_explanation
from supplymind.features.shipments.application.use_cases import CreateShipment

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("")
async def predict(req: PredictionRequest, runtime=Depends(get_champion_runtime), registry=Depends(get_model_registry), predictions=Depends(get_prediction_repository), shipments=Depends(get_shipment_repository)):
    try:
        return await PredictShipment(runtime=runtime, create_shipment=CreateShipment(shipments), record_prediction=RecordPrediction(predictions), model_registry=registry).execute(
            external_id=req.external_id, order_date=req.order_date, features=req.features
        )
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@router.get("")
async def list_predictions(limit: int = Query(50, ge=1, le=200), predictions=Depends(get_prediction_repository), shipments=Depends(get_shipment_repository)):
    rows = await predictions.list_recent(limit=limit)
    result = []
    for p in rows:
        shipment = await shipments.get(p.shipment_id)
        payload = shipment.payload if shipment else {}
        result.append({
            "id": str(p.id), "shipment_id": str(p.shipment_id),
            "external_id": shipment.external_id if shipment else str(p.shipment_id),
            "destination": payload.get("order_city") or payload.get("customer_city") or payload.get("order_country"),
            "delayed": p.delayed, "delay_probability": p.delay_probability, "threshold": p.threshold,
            "risk_level": p.risk_level, "created_at": p.created_at.isoformat() if p.created_at else None,
            "explanation": decision_explanation(p.delay_probability, p.threshold),
        })
    return result
