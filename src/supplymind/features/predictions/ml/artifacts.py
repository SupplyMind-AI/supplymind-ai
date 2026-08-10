"""Model artifact persistence and loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib


# -------------------
# Artifact persistence
# Save a fitted pipeline and its metadata atomically enough for V1.
# -------------------

def save_model_artifact(
    model: Any,
    metadata: dict[str, Any],
    artifact_directory: str | Path,
) -> None:
    """"""

    directory = Path(artifact_directory)
    directory.mkdir(parents=True, exist_ok=True)

    model_path = directory / "model.joblib"
    metadata_path = directory / "metadata.json"

    joblib.dump(model, model_path)
    metadata_path.write_text(
        json.dumps(metadata, indent=2, default=str),
        encoding="utf-8",
    )


# -------------------
# Artifact loading
# -------------------

def load_model_artifact(
    artifact_directory: str | Path,
) -> tuple[Any, dict[str, Any]]:
    """Load a model pipeline and its metadata."""

    directory = Path(artifact_directory)
    model = joblib.load(directory / "model.joblib")
    metadata = json.loads(
        (directory / "metadata.json").read_text(encoding="utf-8")
    )
    return model, metadata
