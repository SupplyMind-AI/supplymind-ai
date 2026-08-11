"""Model registry repository ports."""

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from supplymind.features.model_registry.domain.entities import ModelVersion


class ModelRegistryRepository(ABC):
    """Persistence contract for model versions and champion state."""

    @abstractmethod
    async def add(self, model: ModelVersion) -> ModelVersion:
        """Register one model version."""

    @abstractmethod
    async def get(self, model_id: UUID) -> ModelVersion | None:
        """Find a model version by ID."""

    @abstractmethod
    async def get_by_name_version(
        self,
        name: str,
        version: str,
    ) -> ModelVersion | None:
        """Find a model version by natural key."""

    @abstractmethod
    async def get_champion(self, name: str) -> ModelVersion | None:
        """Return the active champion for a model family."""

    @abstractmethod
    async def promote(self, model_id: UUID) -> ModelVersion:
        """Promote one version and demote the previous champion atomically."""

    @abstractmethod
    async def list_versions(self, name: str) -> list[ModelVersion]:
        """List versions newest first."""
