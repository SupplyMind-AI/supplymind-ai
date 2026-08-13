"""Shipment repository ports."""
from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from supplymind.features.shipments.domain.entities import Shipment

class ShipmentRepository(ABC):
    @abstractmethod
    async def add(self, shipment: Shipment) -> Shipment: ...

    async def update(self, shipment: Shipment) -> Shipment:
        """Optional update hook; legacy/test repositories may remain create-only."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, shipment_id: UUID) -> Shipment | None: ...
    @abstractmethod
    async def get_by_external_id(self, external_id: str) -> Shipment | None: ...
    @abstractmethod
    async def list_recent(self, *, limit: int = 100, offset: int = 0) -> list[Shipment]: ...
