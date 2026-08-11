"""Typed prediction-domain schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# -------------------
# Prediction input
# -------------------

class ShipmentFeatures(BaseModel):
    """Canonical feature payload accepted by the prediction service.

    The API layer may expose a richer shipment schema later; this object
    represents only the data required by the persisted ML pipeline.
    """

    model_config = ConfigDict(extra="forbid")

    shipment_id: str | None = None
    prediction_at: datetime | None = None
    values: dict[str, Any]


# -------------------
# Prediction output
# -------------------

class DelayPrediction(BaseModel):
    """Binary delay prediction returned by the champion pipeline."""

    shipment_id: str | None = None
    delayed: bool
    delay_probability: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    risk_level: str
    model_name: str
    model_version: str


# -------------------
# Model metadata
# -------------------

class ModelMetadata(BaseModel):
    """Metadata persisted with a trained candidate or champion model."""

    model_name: str
    model_version: str
    trained_at: datetime
    source_dataset: str
    target_column: str
    split_timestamp_column: str
    feature_columns: list[str]
    threshold: float
    validation_metrics: dict[str, float]
    test_metrics: dict[str, float] | None = None
