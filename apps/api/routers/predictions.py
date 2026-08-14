from fastapi import APIRouter, Depends, HTTPException, Query

from apps.api.dependencies import (
    get_champion_runtime,
    get_model_registry,
    get_prediction_repository,
    get_shipment_repository,
)
from apps.api.schemas import PredictionRequest
from supplymind.features.predictions.application.persistence import RecordPrediction
from supplymind.features.predictions.application.predict import PredictShipment
from supplymind.features.predictions.domain.risk import decision_explanation
from supplymind.features.shipments.application.use_cases import CreateShipment

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("")
async def predict(
    req: PredictionRequest,
    runtime=Depends(get_champion_runtime),
    registry=Depends(get_model_registry),
    predictions=Depends(get_prediction_repository),
    shipments=Depends(get_shipment_repository),
):
    try:
        result = await PredictShipment(
            runtime=runtime,
            create_shipment=CreateShipment(shipments),
            record_prediction=RecordPrediction(predictions),
            model_registry=registry,
        ).execute(
            external_id=req.external_id,
            order_date=req.order_date,
            features=req.features,
        )

        # Keep the application use case as the source of truth and enrich the
        # HTTP response with the same context already persisted in shipment.payload.
        delayed = bool(result.get("delayed", False))
        return {
            **result,
            "delayed": delayed,
            "is_delayed": delayed,
            "predicted_delay": delayed,
            "origin_city": req.features.get("customer_city"),
            "destination_city": req.features.get("order_city"),
            "customer_city": req.features.get("customer_city"),
            "order_city": req.features.get("order_city"),
            "shipping_mode": req.features.get("shipping_mode"),
            "features": req.features,
        }
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("")
async def list_predictions(
    limit: int = Query(50, ge=1, le=200),
    predictions=Depends(get_prediction_repository),
    shipments=Depends(get_shipment_repository),
):
    rows = await predictions.list_recent(limit=limit)
    result = []

    for prediction in rows:
        shipment = await shipments.get(prediction.shipment_id)
        payload = shipment.payload if shipment else {}

        result.append(
            {
                "id": str(prediction.id),
                "prediction_id": str(prediction.id),
                "shipment_id": str(prediction.shipment_id),
                "external_id": (
                    shipment.external_id
                    if shipment
                    else str(prediction.shipment_id)
                ),
                # Explicit route fields fix the old ambiguous `destination`
                # field and make Command Center + Shipment Intelligence stable.
                "origin_city": payload.get("customer_city"),
                "destination_city": payload.get("order_city"),
                "customer_city": payload.get("customer_city"),
                "order_city": payload.get("order_city"),
                "shipping_mode": payload.get("shipping_mode"),
                "order_country": payload.get("order_country"),
                "customer_country": payload.get("customer_country"),
                "features": payload,
                "delayed": prediction.delayed,
                "is_delayed": prediction.delayed,
                "predicted_delay": prediction.delayed,
                "delay_probability": prediction.delay_probability,
                "threshold": prediction.threshold,
                "risk_level": prediction.risk_level,
                "created_at": (
                    prediction.created_at.isoformat()
                    if prediction.created_at
                    else None
                ),
                "explanation": decision_explanation(
                    prediction.delay_probability,
                    prediction.threshold,
                ),
            }
        )

    return result
