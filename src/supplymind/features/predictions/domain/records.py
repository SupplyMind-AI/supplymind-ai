"""Persisted prediction domain record."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True)
class PredictionRecord:
    """Persisted output of one model scoring operation."""

    shipment_id: UUID
    model_version_id: UUID
    delayed: bool
    delay_probability: float
    threshold: float
    risk_level: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
