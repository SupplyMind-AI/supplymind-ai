"""Register the persisted champion model during application startup."""
from __future__ import annotations
import json
from pathlib import Path
from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.predictions.infrastructure.runtime import ChampionModelRuntime


async def register_champion_if_available(
    *,
    registry,
    model_directory: Path,
) -> None:
    """Ensure the filesystem champion is registered in the model registry.

    Safe to run on every application startup.
    """

    model_directory = Path(model_directory)

    model_path = model_directory / "model.joblib"
    metadata_path = model_directory / "metadata.json"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Champion model missing: {model_path}"
        )

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Champion metadata missing: {metadata_path}"
        )

    metadata = json.loads(
        metadata_path.read_text()
    )

    model_name = metadata["model_name"]
    model_version = metadata.get(
        "model_version",
        "1.0.0",
    )
    threshold = float(
        metadata["threshold"]
    )

    print(
        f"[champion] artifact found: "
        f"{model_name} "
        f"version={model_version} "
        f"threshold={threshold}"
    )

    # Existing repository should decide whether this
    # is an insert or an update/upsert.
    await registry.register_champion(
        model_name=model_name,
        model_version=model_version,
        artifact_path=str(model_path),
        threshold=threshold,
        metadata=metadata,
    )

    print(
        f"[champion] registered successfully: "
        f"{model_name}@{model_version}"
    )
