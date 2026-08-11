"""Supply-chain event application use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from supplymind.features.events.domain.entities import SupplyChainEvent
from supplymind.features.events.domain.repositories import EventRepository


class UpsertEvent:
    """Normalize and persist one event from GDELT or another provider."""

    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        external_id: str,
        source: str,
        event_type: str,
        title: str,
        description: str | None = None,
        severity: float | None = None,
        country: str | None = None,
        region: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        starts_at: datetime | None = None,
        ends_at: datetime | None = None,
        embedding_id: str | None = None,
        raw_payload: dict[str, Any] | None = None,
    ) -> SupplyChainEvent:
        event = SupplyChainEvent(
            external_id=external_id,
            source=source,
            event_type=event_type,
            title=title,
            description=description,
            severity=severity,
            country=country,
            region=region,
            latitude=latitude,
            longitude=longitude,
            starts_at=starts_at,
            ends_at=ends_at,
            embedding_id=embedding_id,
            raw_payload=raw_payload or {},
        )
        return await self.repository.upsert(event)


class ListActiveEvents:
    """Read events for the Event Monitor screen."""

    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        at: datetime,
        limit: int = 200,
    ) -> list[SupplyChainEvent]:
        return await self.repository.list_active(at=at, limit=limit)
