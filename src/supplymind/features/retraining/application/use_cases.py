"""Retraining application use cases.

This phase persists and manages jobs. The actual training worker is added later and can
consume the same repository without changing this interface.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

from supplymind.features.retraining.domain.entities import (
    RetrainingJob,
    RetrainingStatus,
    RetrainingTrigger,
)
from supplymind.features.retraining.domain.repositories import RetrainingRepository


class RequestRetraining:
    """Queue a retraining job from any supported trigger."""

    def __init__(self, repository: RetrainingRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        trigger_type: RetrainingTrigger,
        reason: str,
        base_model_version_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> RetrainingJob:
        job = RetrainingJob(
            trigger_type=trigger_type,
            reason=reason,
            base_model_version_id=base_model_version_id,
            metadata=metadata or {},
        )
        return await self.repository.add(job)


class MarkRetrainingRunning:
    """Move a queued job into running state."""

    def __init__(self, repository: RetrainingRepository) -> None:
        self.repository = repository

    async def execute(self, job_id: UUID) -> RetrainingJob:
        return await self.repository.update_status(
            job_id,
            RetrainingStatus.RUNNING,
        )


class CompleteRetraining:
    """Record successful retraining."""

    def __init__(self, repository: RetrainingRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        job_id: UUID,
        *,
        new_model_version_id: UUID,
    ) -> RetrainingJob:
        return await self.repository.update_status(
            job_id,
            RetrainingStatus.SUCCEEDED,
            new_model_version_id=new_model_version_id,
        )


class FailRetraining:
    """Record retraining failure without losing job history."""

    def __init__(self, repository: RetrainingRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        job_id: UUID,
        *,
        error_message: str,
    ) -> RetrainingJob:
        return await self.repository.update_status(
            job_id,
            RetrainingStatus.FAILED,
            error_message=error_message,
        )
