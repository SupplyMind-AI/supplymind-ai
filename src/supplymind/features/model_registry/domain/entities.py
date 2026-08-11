"""Model registry domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ModelVersion:
    """Registered ML model version."""

    name: str
    version: str
    artifact_uri: str
    target_column: str
    threshold: float
    metrics: dict[str, Any] = field(default_factory=dict)
    feature_columns: list[str] = field(default_factory=list)
    trained_at: datetime | None = None
    is_champion: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
