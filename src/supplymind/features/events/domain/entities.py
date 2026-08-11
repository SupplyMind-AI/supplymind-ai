"""Supply-chain event domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class SupplyChainEvent:
    """Normalized external disruption or logistics event."""

    external_id: str
    source: str
    event_type: str
    title: str
    description: str | None = None
    severity: float | None = None
    country: str | None = None
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    embedding_id: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
