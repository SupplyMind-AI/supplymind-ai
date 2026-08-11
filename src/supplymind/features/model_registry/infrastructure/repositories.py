"""SQLAlchemy model registry repository."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.model_registry.domain.repositories import ModelRegistryRepository
from supplymind.features.model_registry.infrastructure.models import ModelVersionModel


def _to_entity(model: ModelVersionModel) -> ModelVersion:
    return ModelVersion(
        id=model.id,
        name=model.name,
        version=model.version,
        artifact_uri=model.artifact_uri,
        target_column=model.target_column,
        threshold=model.threshold,
        metrics=model.metrics or {},
        feature_columns=model.feature_columns or [],
        trained_at=model.trained_at,
        is_champion=model.is_champion,
        created_at=model.created_at,
    )


class SqlAlchemyModelRegistryRepository(ModelRegistryRepository):
    """PostgreSQL model registry implementation."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, model: ModelVersion) -> ModelVersion:
        record = ModelVersionModel(
            id=model.id,
            name=model.name,
            version=model.version,
            artifact_uri=model.artifact_uri,
            target_column=model.target_column,
            threshold=model.threshold,
            metrics=model.metrics,
            feature_columns=model.feature_columns,
            trained_at=model.trained_at,
            is_champion=model.is_champion,
        )
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return _to_entity(record)

    async def get(self, model_id: UUID) -> ModelVersion | None:
        record = await self.session.get(ModelVersionModel, model_id)
        return _to_entity(record) if record else None

    async def get_by_name_version(
        self,
        name: str,
        version: str,
    ) -> ModelVersion | None:
        result = await self.session.execute(
            select(ModelVersionModel).where(
                ModelVersionModel.name == name,
                ModelVersionModel.version == version,
            )
        )
        record = result.scalar_one_or_none()
        return _to_entity(record) if record else None

    async def get_champion(self, name: str) -> ModelVersion | None:
        result = await self.session.execute(
            select(ModelVersionModel).where(
                ModelVersionModel.name == name,
                ModelVersionModel.is_champion.is_(True),
            )
        )
        record = result.scalar_one_or_none()
        return _to_entity(record) if record else None

    async def promote(self, model_id: UUID) -> ModelVersion:
        target = await self.session.get(ModelVersionModel, model_id)
        if target is None:
            raise LookupError(f"Model version not found: {model_id}")

        await self.session.execute(
            update(ModelVersionModel)
            .where(ModelVersionModel.name == target.name)
            .values(is_champion=False)
        )
        target.is_champion = True
        await self.session.flush()
        await self.session.refresh(target)
        return _to_entity(target)

    async def list_versions(self, name: str) -> list[ModelVersion]:
        result = await self.session.execute(
            select(ModelVersionModel)
            .where(ModelVersionModel.name == name)
            .order_by(ModelVersionModel.created_at.desc())
        )
        return [_to_entity(record) for record in result.scalars()]
