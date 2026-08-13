"""SQLAlchemy event repository."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import and_, or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.events.domain.entities import SupplyChainEvent
from supplymind.features.events.domain.repositories import EventRepository
from supplymind.features.events.infrastructure.models import EventModel


def _to_entity(model: EventModel) -> SupplyChainEvent:
    return SupplyChainEvent(
        id=model.id,
        external_id=model.external_id,
        source=model.source,
        event_type=model.event_type,
        title=model.title,
        description=model.description,
        severity=model.severity,
        country=model.country,
        region=model.region,
        latitude=model.latitude,
        longitude=model.longitude,
        starts_at=model.starts_at,
        ends_at=model.ends_at,
        embedding_id=model.embedding_id,
        raw_payload=model.raw_payload or {},
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class SqlAlchemyEventRepository(EventRepository):
    """PostgreSQL EventRepository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert(self, event: SupplyChainEvent) -> SupplyChainEvent:
        statement = (
            insert(EventModel)
            .values(
                id=event.id,
                external_id=event.external_id,
                source=event.source,
                event_type=event.event_type,
                title=event.title,
                description=event.description,
                severity=event.severity,
                country=event.country,
                region=event.region,
                latitude=event.latitude,
                longitude=event.longitude,
                starts_at=event.starts_at,
                ends_at=event.ends_at,
                embedding_id=event.embedding_id,
                raw_payload=event.raw_payload,
            )
            .on_conflict_do_update(
                constraint="uq_events_source_external",
                set_={
                    "event_type": event.event_type,
                    "title": event.title,
                    "description": event.description,
                    "severity": event.severity,
                    "country": event.country,
                    "region": event.region,
                    "latitude": event.latitude,
                    "longitude": event.longitude,
                    "starts_at": event.starts_at,
                    "ends_at": event.ends_at,
                    "embedding_id": event.embedding_id,
                    "raw_payload": event.raw_payload,
                    "updated_at": datetime.now().astimezone(),
                },
            )
            .returning(EventModel)
        )

        result = await self.session.execute(statement)
        record = result.scalar_one()
        await self.session.flush()
        return _to_entity(record)

    async def list_active(
        self,
        *,
        at: datetime,
        limit: int = 200,
    ) -> list[SupplyChainEvent]:
        result = await self.session.execute(
            select(EventModel)
            .where(
                and_(
                    or_(EventModel.starts_at.is_(None), EventModel.starts_at <= at),
                    or_(EventModel.ends_at.is_(None), EventModel.ends_at >= at),
                )
            )
            .order_by(EventModel.severity.desc().nullslast(), EventModel.created_at.desc())
            .limit(limit)
        )
        return [_to_entity(record) for record in result.scalars()]

    async def list_recent(self, *, limit: int = 200) -> list[SupplyChainEvent]:
        result = await self.session.execute(
            select(EventModel)
            .order_by(EventModel.created_at.desc())
            .limit(limit)
        )
        return [_to_entity(record) for record in result.scalars()]
