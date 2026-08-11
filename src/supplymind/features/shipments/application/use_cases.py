"""Shipment application use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from supplymind.features.shipments.domain.entities import Shipment
from supplymind.features.shipments.domain.repositories import ShipmentRepository


# -------------------
# Create / update
# -------------------

class CreateShipment:
    """Create a shipment unless its external ID already exists."""

    def __init__(self, repository: ShipmentRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        external_id: str,
        order_date: datetime,
        source: str = "syndelay",
        status: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Shipment:
        existing = await self.repository.get_by_external_id(external_id)
        if existing is not None:
            return existing

        shipment = Shipment(
            external_id=external_id,
            order_date=order_date,
            source=source,
            status=status,
            payload=payload or {},
        )
        return await self.repository.add(shipment)


# -------------------
# Queries
# -------------------

class GetShipment:
    """Retrieve one shipment."""

    def __init__(self, repository: ShipmentRepository) -> None:
        self.repository = repository

    async def execute(self, shipment_id: UUID) -> Shipment | None:
        return await self.repository.get(shipment_id)


class ListRecentShipments:
    """List recent persisted shipments."""

    def __init__(self, repository: ShipmentRepository) -> None:
        self.repository = repository

    async def execute(self, *, limit: int = 100, offset: int = 0) -> list[Shipment]:
        return await self.repository.list_recent(limit=limit, offset=offset)
