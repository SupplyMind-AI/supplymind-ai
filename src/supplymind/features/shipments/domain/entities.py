"""Shipment domain entities."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Shipment:
    """Canonical persisted shipment record."""

    external_id: str
    order_date: datetime
    source: str = "syndelay"
    status: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime | None = None
    updated_at: datetime | None = None
