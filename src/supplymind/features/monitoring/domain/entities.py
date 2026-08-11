"""Model monitoring domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class MonitoringSnapshot:
    """Aggregated monitoring statistics for one observation window."""

    model_version_id: UUID
    window_start: datetime
    window_end: datetime
    sample_count: int
    delayed_prediction_rate: float
    average_probability: float
    metrics: dict[str, Any] = field(default_factory=dict)
    drift_metrics: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
