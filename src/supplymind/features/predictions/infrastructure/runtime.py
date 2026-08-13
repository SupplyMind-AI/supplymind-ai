"""Runtime adapter for the persisted champion sklearn pipeline."""
from __future__ import annotations
import json
from pathlib import Path
import joblib
import pandas as pd
from supplymind.features.predictions.domain.risk import risk_level_for_probability


class ChampionModelRuntime:
    """Load one persisted champion and expose a stable prediction API."""

    def __init__(self, model_directory: str | Path) -> None:
        directory = Path(model_directory)
        model_path = directory / "model.joblib"
        metadata_path = directory / "metadata.json"
        if not model_path.exists() or not metadata_path.exists():
            raise FileNotFoundError(f"Champion artifact incomplete: {directory}")
        self.pipeline = joblib.load(model_path)
        self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    @property
    def threshold(self) -> float:
        return float(self.metadata.get("threshold", 0.5))

    @property
    def model_name(self) -> str:
        return str(self.metadata.get("model_name", "delay_prediction"))

    @property
    def model_version(self) -> str:
        return str(self.metadata.get("model_version", "1.0.0"))

    def predict(self, features: dict) -> dict:
        probability = float(self.pipeline.predict_proba(pd.DataFrame([features]))[0, 1])
        delayed = probability >= self.threshold
        return {
            "delayed": bool(delayed),
            "delay_probability": probability,
            "threshold": self.threshold,
            "risk_level": risk_level_for_probability(probability, self.threshold),
            "model_name": self.model_name,
            "model_version": self.model_version,
        }
