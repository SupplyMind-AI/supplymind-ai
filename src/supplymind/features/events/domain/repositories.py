"""Event repository ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from supplymind.features.events.domain.entities import SupplyChainEvent


class EventRepository(ABC):
    """Persistence contract for external supply-chain events."""

    @abstractmethod
    async def upsert(self, event: SupplyChainEvent) -> SupplyChainEvent:
        """Insert or update by source + external ID."""

    @abstractmethod
    async def list_active(
        self,
        *,
        at: datetime,
        limit: int = 200,
    ) -> list[SupplyChainEvent]:
        """Return events active at a point in time."""

    @abstractmethod
    async def list_recent(self, *, limit: int = 200) -> list[SupplyChainEvent]:
        """Return recently observed events."""
