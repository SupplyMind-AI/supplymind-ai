"""Retraining domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4


class RetrainingTrigger(StrEnum):
    """Supported retraining trigger categories."""

    SCHEDULED = "scheduled"
    DRIFT = "drift"
    MANUAL = "manual"
    NEW_DATA = "new_data"


class RetrainingStatus(StrEnum):
    """Retraining job lifecycle."""

    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True)
class RetrainingJob:
    """Persisted retraining job state."""

    trigger_type: RetrainingTrigger
    reason: str
    status: RetrainingStatus = RetrainingStatus.QUEUED
    base_model_version_id: UUID | None = None
    new_model_version_id: UUID | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    requested_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    id: UUID = field(default_factory=uuid4)
