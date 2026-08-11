"""Monitoring repository ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from supplymind.features.monitoring.domain.entities import MonitoringSnapshot


class MonitoringRepository(ABC):
    """Persistence contract for monitoring snapshots."""

    @abstractmethod
    async def add(self, snapshot: MonitoringSnapshot) -> MonitoringSnapshot:
        """Persist one monitoring snapshot."""

    @abstractmethod
    async def list_for_model(
        self,
        model_version_id: UUID,
        *,
        limit: int = 100,
    ) -> list[MonitoringSnapshot]:
        """Return recent snapshots for one model version."""
