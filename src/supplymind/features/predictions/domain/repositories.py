"""Prediction persistence ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from supplymind.features.predictions.domain.records import PredictionRecord


class PredictionRepository(ABC):
    """Persistence contract for model predictions."""

    @abstractmethod
    async def add(self, prediction: PredictionRecord) -> PredictionRecord:
        """Persist a prediction."""

    @abstractmethod
    async def get_latest_for_shipment(
        self,
        shipment_id: UUID,
    ) -> PredictionRecord | None:
        """Return the latest prediction for a shipment."""

    @abstractmethod
    async def list_recent(self, *, limit: int = 100) -> list[PredictionRecord]:
        """Return recent predictions."""
