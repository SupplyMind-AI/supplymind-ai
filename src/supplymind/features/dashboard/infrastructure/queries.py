"""Read-optimized dashboard queries."""
from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import case, func, or_, select
from supplymind.features.dashboard.domain.schemas import (
    DashboardEvent, DashboardPrediction, DashboardSummary, RiskDistribution,
)
from supplymind.features.events.infrastructure.models import EventModel
from supplymind.features.model_registry.infrastructure.models import ModelVersionModel
from supplymind.features.predictions.infrastructure.models import PredictionModel
from supplymind.features.predictions.domain.risk import decision_explanation
from supplymind.features.retraining.infrastructure.models import RetrainingJobModel
from supplymind.features.shipments.infrastructure.models import ShipmentModel


class DashboardQueryService:
    def __init__(self, session):
        self.session = session

    async def summary(self) -> DashboardSummary:
        shipment_count = await self.session.scalar(select(func.count()).select_from(ShipmentModel))
        prediction_count = await self.session.scalar(select(func.count()).select_from(PredictionModel))
        stats = (await self.session.execute(select(
            func.avg(case((PredictionModel.delayed.is_(True), 1.0), else_=0.0)),
            func.avg(PredictionModel.delay_probability),
        ))).one()

        now = datetime.now(timezone.utc)
        active_event_count = await self.session.scalar(
            select(func.count()).select_from(EventModel).where(
                or_(EventModel.starts_at.is_(None), EventModel.starts_at <= now),
                or_(EventModel.ends_at.is_(None), EventModel.ends_at >= now),
            )
        )
        queued = await self.session.scalar(
            select(func.count()).select_from(RetrainingJobModel).where(
                RetrainingJobModel.status.in_(["queued", "running"])
            )
        )
        champion = (await self.session.execute(
            select(ModelVersionModel).where(ModelVersionModel.is_champion.is_(True))
            .order_by(ModelVersionModel.created_at.desc()).limit(1)
        )).scalar_one_or_none()

        risk_rows = (await self.session.execute(
            select(PredictionModel.risk_level, func.count())
            .group_by(PredictionModel.risk_level)
        )).all()
        risk = {str(level): int(count) for level, count in risk_rows}

        recent_rows = (await self.session.execute(
            select(PredictionModel, ShipmentModel)
            .join(ShipmentModel, ShipmentModel.id == PredictionModel.shipment_id)
            .order_by(PredictionModel.created_at.desc()).limit(8)
        )).all()
        recent_predictions = []
        for prediction, shipment in recent_rows:
            payload = shipment.payload or {}
            destination = payload.get("order_city") or payload.get("customer_city") or payload.get("order_country")
            recent_predictions.append(DashboardPrediction(
                external_id=shipment.external_id,
                destination=destination,
                delayed=prediction.delayed,
                delay_probability=prediction.delay_probability,
                threshold=prediction.threshold,
                risk_level=prediction.risk_level,
                explanation=decision_explanation(prediction.delay_probability, prediction.threshold),
                created_at=prediction.created_at.isoformat() if prediction.created_at else None,
            ))

        events = (await self.session.execute(
            select(EventModel).where(
                or_(EventModel.starts_at.is_(None), EventModel.starts_at <= now),
                or_(EventModel.ends_at.is_(None), EventModel.ends_at >= now),
            ).order_by(EventModel.severity.desc().nullslast(), EventModel.created_at.desc()).limit(6)
        )).scalars().all()

        return DashboardSummary(
            shipment_count=int(shipment_count or 0),
            prediction_count=int(prediction_count or 0),
            delayed_prediction_rate=float(stats[0] or 0),
            average_delay_probability=float(stats[1] or 0),
            active_event_count=int(active_event_count or 0),
            queued_retraining_jobs=int(queued or 0),
            champion_model_name=champion.name if champion else None,
            champion_model_version=champion.version if champion else None,
            champion_threshold=champion.threshold if champion else None,
            risk_distribution=RiskDistribution(
                low=risk.get("low", 0), medium=risk.get("medium", 0), high=risk.get("high", 0)
            ),
            recent_predictions=recent_predictions,
            recent_events=[DashboardEvent(
                id=str(e.id), title=e.title, event_type=e.event_type, severity=e.severity,
                country=e.country, region=e.region,
            ) for e in events],
        )
