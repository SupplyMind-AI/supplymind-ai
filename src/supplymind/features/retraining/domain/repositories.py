"""Retraining repository ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from supplymind.features.retraining.domain.entities import (
    RetrainingJob,
    RetrainingStatus,
)


class RetrainingRepository(ABC):
    """Persistence contract for retraining jobs."""

    @abstractmethod
    async def add(self, job: RetrainingJob) -> RetrainingJob:
        """Create a retraining job."""

    @abstractmethod
    async def get(self, job_id: UUID) -> RetrainingJob | None:
        """Find a retraining job."""

    @abstractmethod
    async def update_status(
        self,
        job_id: UUID,
        status: RetrainingStatus,
        *,
        new_model_version_id: UUID | None = None,
        error_message: str | None = None,
    ) -> RetrainingJob:
        """Advance retraining lifecycle state."""

    @abstractmethod
    async def list_recent(self, *, limit: int = 100) -> list[RetrainingJob]:
        """Return recent retraining jobs."""
