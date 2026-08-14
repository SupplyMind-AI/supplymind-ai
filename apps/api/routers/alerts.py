from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException

from apps.api.dependencies import (
    get_event_repository,
    get_prediction_repository,
    get_shipment_repository,
)

router = APIRouter(prefix="/alerts", tags=["alerts"])

# Presentation-safe V1 acknowledgement state. It preserves the existing alert
# derivation and avoids a last-minute DB migration. V1.1 should persist this.
_acknowledged_alert_ids: set[str] = set()


@router.get("")
async def alerts(
    predictions=Depends(get_prediction_repository),
    shipments=Depends(get_shipment_repository),
    events=Depends(get_event_repository),
):
    items = []

    for prediction in await predictions.list_recent(limit=100):
        if prediction.risk_level not in {"high", "medium"}:
            continue

        shipment = await shipments.get(prediction.shipment_id)
        payload = shipment.payload if shipment else {}
        alert_id = f"prediction:{prediction.id}"

        items.append(
            {
                "id": alert_id,
                "kind": "prediction",
                "severity": prediction.risk_level,
                "title": (
                    f"{shipment.external_id if shipment else prediction.shipment_id} "
                    f"· {'delay likely' if prediction.delayed else 'elevated delay risk'}"
                ),
                "detail": (
                    f"Delay score {prediction.delay_probability:.1%} vs "
                    f"threshold {prediction.threshold:.1%}"
                ),
                "shipment_id": str(prediction.shipment_id),
                "prediction_id": str(prediction.id),
                "external_id": (
                    shipment.external_id if shipment else str(prediction.shipment_id)
                ),
                "origin_city": payload.get("customer_city"),
                "destination_city": payload.get("order_city"),
                "shipping_mode": payload.get("shipping_mode"),
                "delay_probability": prediction.delay_probability,
                "threshold": prediction.threshold,
                "delayed": prediction.delayed,
                "risk_level": prediction.risk_level,
                "acknowledged": alert_id in _acknowledged_alert_ids,
                "created_at": (
                    prediction.created_at.isoformat()
                    if prediction.created_at
                    else None
                ),
            }
        )

    for event in await events.list_active(
        at=datetime.now(timezone.utc),
        limit=100,
    ):
        if (event.severity or 0) < 0.7:
            continue

        alert_id = f"event:{event.id}"
        items.append(
            {
                "id": alert_id,
                "kind": "event",
                "severity": "high" if (event.severity or 0) >= 0.8 else "medium",
                "title": event.title,
                "detail": (
                    f"{event.event_type} · {event.country or 'Unknown'} · "
                    f"severity {(event.severity or 0):.2f}"
                ),
                "acknowledged": alert_id in _acknowledged_alert_ids,
                "created_at": event.created_at.isoformat() if event.created_at else None,
            }
        )

    return sorted(
        items,
        key=lambda item: item.get("created_at") or "",
        reverse=True,
    )[:50]


@router.patch("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str):
    if not alert_id:
        raise HTTPException(status_code=400, detail="alert_id is required")

    _acknowledged_alert_ids.add(alert_id)
    return {"id": alert_id, "acknowledged": True}
