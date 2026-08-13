"""Monitoring application use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from supplymind.features.monitoring.domain.entities import MonitoringSnapshot
from supplymind.features.monitoring.domain.repositories import MonitoringRepository


class RecordMonitoringSnapshot:
    """Persist aggregated model-monitoring statistics."""

    def __init__(self, repository: MonitoringRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        model_version_id: UUID,
        window_start: datetime,
        window_end: datetime,
        sample_count: int,
        delayed_prediction_rate: float,
        average_probability: float,
        metrics: dict[str, Any] | None = None,
        drift_metrics: dict[str, Any] | None = None,
    ) -> MonitoringSnapshot:
        if window_end <= window_start:
            raise ValueError("window_end must be after window_start.")
        if sample_count < 0:
            raise ValueError("sample_count must be non-negative.")

        snapshot = MonitoringSnapshot(
            model_version_id=model_version_id,
            window_start=window_start,
            window_end=window_end,
            sample_count=sample_count,
            delayed_prediction_rate=delayed_prediction_rate,
            average_probability=average_probability,
            metrics=metrics or {},
            drift_metrics=drift_metrics or {},
        )
        return await self.repository.add(snapshot)
