"""Versioned model artifact persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib


# -------------------
# Save artifact
# -------------------

def save_model_artifact(
    model: Any,
    metadata: dict,
    directory: str | Path,
) -> None:
    """Persist preprocessing + estimator together with metadata."""

    artifact_directory = Path(directory)
    artifact_directory.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, artifact_directory / "model.joblib")
    (artifact_directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, default=str),
        encoding="utf-8",
    )


# -------------------
# Load artifact
# -------------------

def load_model_artifact(
    directory: str | Path,
) -> tuple[Any, dict]:
    """Load a persisted model pipeline and metadata."""

    artifact_directory = Path(directory)

    model = joblib.load(artifact_directory / "model.joblib")
    metadata = json.loads(
        (artifact_directory / "metadata.json").read_text(encoding="utf-8")
    )
    return model, metadata
