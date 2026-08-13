"""Model registry application use cases."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.model_registry.domain.repositories import ModelRegistryRepository


class RegisterModelVersion:
    """Register a trained model artifact without promoting it."""

    def __init__(self, repository: ModelRegistryRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        *,
        name: str,
        version: str,
        artifact_uri: str,
        target_column: str,
        threshold: float,
        metrics: dict[str, Any],
        feature_columns: list[str],
        trained_at: datetime | None = None,
    ) -> ModelVersion:
        existing = await self.repository.get_by_name_version(name, version)
        if existing is not None:
            return existing

        model = ModelVersion(
            name=name,
            version=version,
            artifact_uri=artifact_uri,
            target_column=target_column,
            threshold=threshold,
            metrics=metrics,
            feature_columns=feature_columns,
            trained_at=trained_at,
        )
        return await self.repository.add(model)


class PromoteChampion:
    """Promote a registered model version."""

    def __init__(self, repository: ModelRegistryRepository) -> None:
        self.repository = repository

    async def execute(self, model_id: UUID) -> ModelVersion:
        return await self.repository.promote(model_id)


class GetChampion:
    """Read the active champion."""

    def __init__(self, repository: ModelRegistryRepository) -> None:
        self.repository = repository

    async def execute(self, name: str) -> ModelVersion | None:
        return await self.repository.get_champion(name)
