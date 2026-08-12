"""Register the persisted champion model during application startup."""
from __future__ import annotations
from pathlib import Path
from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.predictions.infrastructure.runtime import ChampionModelRuntime


async def register_champion_if_available(*, registry, model_directory: str | Path) -> bool:
    directory = Path(model_directory)
    if not (directory / "model.joblib").exists() or not (directory / "metadata.json").exists():
        return False
    runtime = ChampionModelRuntime(directory)
    existing = await registry.get_by_name_version(runtime.model_name, runtime.model_version)
    if existing is None:
        existing = await registry.add(ModelVersion(
            name=runtime.model_name,
            version=runtime.model_version,
            artifact_uri=str(directory),
            target_column="is_delayed",
            threshold=runtime.threshold,
            metrics=runtime.metadata.get("test_metrics", {}),
            feature_columns=runtime.metadata.get("feature_columns", []),
            is_champion=False,
        ))
    if not existing.is_champion:
        await registry.promote(existing.id)
    return True
