"""SQLAlchemy shipment repository."""
from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from supplymind.features.shipments.domain.entities import Shipment
from supplymind.features.shipments.domain.repositories import ShipmentRepository
from supplymind.features.shipments.infrastructure.models import ShipmentModel

def _to_entity(model: ShipmentModel) -> Shipment:
    return Shipment(id=model.id,external_id=model.external_id,order_date=model.order_date,source=model.source,status=model.status,payload=model.payload or {},created_at=model.created_at,updated_at=model.updated_at)

class SqlAlchemyShipmentRepository(ShipmentRepository):
    def __init__(self, session: AsyncSession) -> None:self.session=session
    async def add(self, shipment: Shipment) -> Shipment:
        model=ShipmentModel(id=shipment.id,external_id=shipment.external_id,order_date=shipment.order_date,source=shipment.source,status=shipment.status,payload=shipment.payload)
        self.session.add(model);await self.session.flush();await self.session.refresh(model);return _to_entity(model)
    async def update(self, shipment: Shipment) -> Shipment:
        model=await self.session.get(ShipmentModel,shipment.id)
        if model is None:raise LookupError(f"Shipment not found: {shipment.id}")
        model.order_date=shipment.order_date;model.source=shipment.source;model.status=shipment.status;model.payload=shipment.payload
        await self.session.flush();await self.session.refresh(model);return _to_entity(model)
    async def get(self, shipment_id: UUID) -> Shipment | None:
        model=await self.session.get(ShipmentModel,shipment_id);return _to_entity(model) if model else None
    async def get_by_external_id(self, external_id: str) -> Shipment | None:
        result=await self.session.execute(select(ShipmentModel).where(ShipmentModel.external_id==external_id));model=result.scalar_one_or_none();return _to_entity(model) if model else None
    async def list_recent(self, *, limit: int=100, offset: int=0) -> list[Shipment]:
        result=await self.session.execute(select(ShipmentModel).order_by(ShipmentModel.order_date.desc()).limit(limit).offset(offset));return [_to_entity(m) for m in result.scalars()]
