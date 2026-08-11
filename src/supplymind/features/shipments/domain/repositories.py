"""Shipment repository ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from supplymind.features.shipments.domain.entities import Shipment


class ShipmentRepository(ABC):
    """Persistence contract used by shipment application services."""

    @abstractmethod
    async def add(self, shipment: Shipment) -> Shipment:
        """Persist a shipment."""

    @abstractmethod
    async def get(self, shipment_id: UUID) -> Shipment | None:
        """Find a shipment by internal ID."""

    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> Shipment | None:
        """Find a shipment by external business ID."""

    @abstractmethod
    async def list_recent(self, *, limit: int = 100, offset: int = 0) -> list[Shipment]:
        """Return recent shipments."""
