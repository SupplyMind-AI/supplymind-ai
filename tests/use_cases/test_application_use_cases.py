"""Fast unit tests for Phase 3 application services."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from supplymind.features.model_registry.application.use_cases import RegisterModelVersion
from supplymind.features.model_registry.domain.repositories import ModelRegistryRepository
from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.shipments.application.use_cases import CreateShipment
from supplymind.features.shipments.domain.entities import Shipment
from supplymind.features.shipments.domain.repositories import ShipmentRepository


class FakeShipmentRepository(ShipmentRepository):
    def __init__(self) -> None:
        self.items: dict[UUID, Shipment] = {}

    async def add(self, shipment: Shipment) -> Shipment:
        self.items[shipment.id] = shipment
        return shipment

    async def get(self, shipment_id: UUID) -> Shipment | None:
        return self.items.get(shipment_id)

    async def get_by_external_id(self, external_id: str) -> Shipment | None:
        return next(
            (item for item in self.items.values() if item.external_id == external_id),
            None,
        )

    async def list_recent(self, *, limit: int = 100, offset: int = 0) -> list[Shipment]:
        return list(self.items.values())[offset: offset + limit]


class FakeModelRegistryRepository(ModelRegistryRepository):
    def __init__(self) -> None:
        self.items: dict[UUID, ModelVersion] = {}

    async def add(self, model: ModelVersion) -> ModelVersion:
        self.items[model.id] = model
        return model

    async def get(self, model_id: UUID) -> ModelVersion | None:
        return self.items.get(model_id)

    async def get_by_name_version(self, name: str, version: str) -> ModelVersion | None:
        return next(
            (
                item for item in self.items.values()
                if item.name == name and item.version == version
            ),
            None,
        )

    async def get_champion(self, name: str) -> ModelVersion | None:
        return next(
            (
                item for item in self.items.values()
                if item.name == name and item.is_champion
            ),
            None,
        )

    async def promote(self, model_id: UUID) -> ModelVersion:
        model = self.items[model_id]
        promoted = ModelVersion(**{
            **model.__dict__,
            "is_champion": True,
        })
        self.items[model_id] = promoted
        return promoted

    async def list_versions(self, name: str) -> list[ModelVersion]:
        return [item for item in self.items.values() if item.name == name]


@pytest.mark.asyncio
async def test_create_shipment_is_idempotent_by_external_id():
    repository = FakeShipmentRepository()
    use_case = CreateShipment(repository)

    first = await use_case.execute(
        external_id="ORDER-1",
        order_date=datetime(2026, 8, 11, tzinfo=timezone.utc),
    )
    second = await use_case.execute(
        external_id="ORDER-1",
        order_date=datetime(2026, 8, 11, tzinfo=timezone.utc),
    )

    assert first.id == second.id
    assert len(repository.items) == 1


@pytest.mark.asyncio
async def test_register_model_version_is_idempotent():
    repository = FakeModelRegistryRepository()
    use_case = RegisterModelVersion(repository)

    first = await use_case.execute(
        name="delay_prediction",
        version="1.0.0",
        artifact_uri="models/champion",
        target_column="is_delayed",
        threshold=0.5,
        metrics={"f1": 0.70},
        feature_columns=["shipping_mode"],
    )
    second = await use_case.execute(
        name="delay_prediction",
        version="1.0.0",
        artifact_uri="models/champion",
        target_column="is_delayed",
        threshold=0.5,
        metrics={"f1": 0.70},
        feature_columns=["shipping_mode"],
    )

    assert first.id == second.id
    assert len(repository.items) == 1
