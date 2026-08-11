"""SQLAlchemy monitoring repository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.monitoring.domain.entities import MonitoringSnapshot
from supplymind.features.monitoring.domain.repositories import MonitoringRepository
from supplymind.features.monitoring.infrastructure.models import MonitoringSnapshotModel


def _to_entity(model: MonitoringSnapshotModel) -> MonitoringSnapshot:
    return MonitoringSnapshot(
        id=model.id,
        model_version_id=model.model_version_id,
        window_start=model.window_start,
        window_end=model.window_end,
        sample_count=model.sample_count,
        delayed_prediction_rate=model.delayed_prediction_rate,
        average_probability=model.average_probability,
        metrics=model.metrics or {},
        drift_metrics=model.drift_metrics or {},
        created_at=model.created_at,
    )


class SqlAlchemyMonitoringRepository(MonitoringRepository):
    """PostgreSQL MonitoringRepository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, snapshot: MonitoringSnapshot) -> MonitoringSnapshot:
        record = MonitoringSnapshotModel(
            id=snapshot.id,
            model_version_id=snapshot.model_version_id,
            window_start=snapshot.window_start,
            window_end=snapshot.window_end,
            sample_count=snapshot.sample_count,
            delayed_prediction_rate=snapshot.delayed_prediction_rate,
            average_probability=snapshot.average_probability,
            metrics=snapshot.metrics,
            drift_metrics=snapshot.drift_metrics,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return _to_entity(record)

    async def list_for_model(
        self,
        model_version_id: UUID,
        *,
        limit: int = 100,
    ) -> list[MonitoringSnapshot]:
        result = await self.session.execute(
            select(MonitoringSnapshotModel)
            .where(MonitoringSnapshotModel.model_version_id == model_version_id)
            .order_by(MonitoringSnapshotModel.window_end.desc())
            .limit(limit)
        )
        return [_to_entity(record) for record in result.scalars()]
