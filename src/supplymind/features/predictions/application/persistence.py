"""Prediction persistence application services."""

from __future__ import annotations

from uuid import UUID

from supplymind.features.predictions.domain.records import PredictionRecord
from supplymind.features.predictions.domain.repositories import PredictionRepository


class RecordPrediction:
    """Persist an already-computed delay prediction."""

    def __init__(self, repository: PredictionRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        shipment_id: UUID,
        model_version_id: UUID,
        delayed: bool,
        delay_probability: float,
        threshold: float,
        risk_level: str,
    ) -> PredictionRecord:
        if not 0.0 <= delay_probability <= 1.0:
            raise ValueError("delay_probability must be between 0 and 1.")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1.")

        record = PredictionRecord(
            shipment_id=shipment_id,
            model_version_id=model_version_id,
            delayed=delayed,
            delay_probability=delay_probability,
            threshold=threshold,
            risk_level=risk_level,
        )
        return await self.repository.add(record)
