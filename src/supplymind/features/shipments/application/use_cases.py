"""Shipment application use cases."""
from __future__ import annotations
from dataclasses import replace
from datetime import datetime
from typing import Any
from uuid import UUID
from supplymind.features.shipments.domain.entities import Shipment
from supplymind.features.shipments.domain.repositories import ShipmentRepository

class CreateShipment:
    """Create a shipment, refreshing current data when the repository supports updates."""
    def __init__(self, repository: ShipmentRepository) -> None:self.repository=repository
    async def execute(self, *, external_id:str, order_date:datetime, source:str="syndelay", status:str|None=None, payload:dict[str,Any]|None=None) -> Shipment:
        existing=await self.repository.get_by_external_id(external_id)
        if existing is not None:
            if type(self.repository).update is not ShipmentRepository.update:
                return await self.repository.update(replace(existing,order_date=order_date,source=source,status=status,payload=payload or {}))
            return existing
        return await self.repository.add(Shipment(external_id=external_id,order_date=order_date,source=source,status=status,payload=payload or {}))

class GetShipment:
    def __init__(self, repository: ShipmentRepository) -> None:self.repository=repository
    async def execute(self, shipment_id: UUID) -> Shipment | None:return await self.repository.get(shipment_id)

class ListRecentShipments:
    def __init__(self, repository: ShipmentRepository) -> None:self.repository=repository
    async def execute(self, *, limit:int=100, offset:int=0) -> list[Shipment]:return await self.repository.list_recent(limit=limit,offset=offset)
