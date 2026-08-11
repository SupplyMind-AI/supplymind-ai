"""SQLAlchemy retraining repository."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.retraining.domain.entities import (
    RetrainingJob,
    RetrainingStatus,
    RetrainingTrigger,
)
from supplymind.features.retraining.domain.repositories import RetrainingRepository
from supplymind.features.retraining.infrastructure.models import RetrainingJobModel


def _to_entity(model: RetrainingJobModel) -> RetrainingJob:
    return RetrainingJob(
        id=model.id,
        trigger_type=RetrainingTrigger(model.trigger_type),
        status=RetrainingStatus(model.status),
        reason=model.reason,
        base_model_version_id=model.base_model_version_id,
        new_model_version_id=model.new_model_version_id,
        metadata=model.job_metadata or {},
        error_message=model.error_message,
        requested_at=model.requested_at,
        started_at=model.started_at,
        completed_at=model.completed_at,
    )


class SqlAlchemyRetrainingRepository(RetrainingRepository):
    """PostgreSQL RetrainingRepository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, job: RetrainingJob) -> RetrainingJob:
        record = RetrainingJobModel(
            id=job.id,
            trigger_type=job.trigger_type.value,
            status=job.status.value,
            reason=job.reason,
            base_model_version_id=job.base_model_version_id,
            new_model_version_id=job.new_model_version_id,
            job_metadata=job.metadata,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return _to_entity(record)

    async def get(self, job_id: UUID) -> RetrainingJob | None:
        record = await self.session.get(RetrainingJobModel, job_id)
        return _to_entity(record) if record else None

    async def update_status(
        self,
        job_id: UUID,
        status: RetrainingStatus,
        *,
        new_model_version_id: UUID | None = None,
        error_message: str | None = None,
    ) -> RetrainingJob:
        record = await self.session.get(RetrainingJobModel, job_id)
        if record is None:
            raise LookupError(f"Retraining job not found: {job_id}")

        now = datetime.now(timezone.utc)
        record.status = status.value

        if status == RetrainingStatus.RUNNING:
            record.started_at = now
        elif status in {RetrainingStatus.SUCCEEDED, RetrainingStatus.FAILED}:
            record.completed_at = now

        if new_model_version_id is not None:
            record.new_model_version_id = new_model_version_id

        if error_message is not None:
            record.error_message = error_message

        await self.session.flush()
        await self.session.refresh(record)
        return _to_entity(record)

    async def list_recent(self, *, limit: int = 100) -> list[RetrainingJob]:
        result = await self.session.execute(
            select(RetrainingJobModel)
            .order_by(RetrainingJobModel.requested_at.desc())
            .limit(limit)
        )
        return [_to_entity(record) for record in result.scalars()]
