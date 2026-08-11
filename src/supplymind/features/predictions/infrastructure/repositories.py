"""SQLAlchemy prediction repository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.predictions.domain.records import PredictionRecord
from supplymind.features.predictions.domain.repositories import PredictionRepository
from supplymind.features.predictions.infrastructure.models import PredictionModel


def _to_entity(model: PredictionModel) -> PredictionRecord:
    return PredictionRecord(
        id=model.id,
        shipment_id=model.shipment_id,
        model_version_id=model.model_version_id,
        delayed=model.delayed,
        delay_probability=model.delay_probability,
        threshold=model.threshold,
        risk_level=model.risk_level,
        created_at=model.created_at,
    )


class SqlAlchemyPredictionRepository(PredictionRepository):
    """PostgreSQL implementation of PredictionRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, prediction: PredictionRecord) -> PredictionRecord:
        record = PredictionModel(
            id=prediction.id,
            shipment_id=prediction.shipment_id,
            model_version_id=prediction.model_version_id,
            delayed=prediction.delayed,
            delay_probability=prediction.delay_probability,
            threshold=prediction.threshold,
            risk_level=prediction.risk_level,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return _to_entity(record)

    async def get_latest_for_shipment(
        self,
        shipment_id: UUID,
    ) -> PredictionRecord | None:
        result = await self.session.execute(
            select(PredictionModel)
            .where(PredictionModel.shipment_id == shipment_id)
            .order_by(PredictionModel.created_at.desc())
            .limit(1)
        )
        record = result.scalar_one_or_none()
        return _to_entity(record) if record else None

    async def list_recent(self, *, limit: int = 100) -> list[PredictionRecord]:
        result = await self.session.execute(
            select(PredictionModel)
            .order_by(PredictionModel.created_at.desc())
            .limit(limit)
        )
        return [_to_entity(record) for record in result.scalars()]
