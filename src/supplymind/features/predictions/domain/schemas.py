"""Domain schemas for shipment-delay prediction."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# -------------------
# Canonical shipment input
# This schema is used for validation, feature engineering, training, and inference.
# This schema intentionally contains only stable, business-level fields.
# Source-specific datasets such as SynDelay must be mapped into this schema
# before validation, feature engineering, training, or inference.
# -------------------

class ShipmentRecord(BaseModel):

    model_config = ConfigDict(extra="allow")

    shipment_id: str
    prediction_at: datetime | None = None
    origin_country: str | None = None
    destination_country: str | None = None
    planned_departure_at: datetime | None = None
    planned_delivery_at: datetime | None = None
    carrier: str | None = None
    transport_mode: str | None = None
    planned_lead_time_days: float | None = None
    weather_severity: float | None = Field(default=None, ge=0.0)
    is_delayed: int | None = Field(default=None, ge=0, le=1)


# -------------------
# Prediction response
# Prediction result returned by the champion model.
# -------------------

class DelayPrediction(BaseModel):

    shipment_id: str
    delayed: bool
    delay_probability: float = Field(ge=0.0, le=1.0)
    risk_level: str
    model_version: str
    risk_drivers: list[dict[str, Any]] = Field(default_factory=list)


# -------------------
# Model metadata
# Metadata stored alongside the champion model artifact.
# -------------------

class ModelMetadata(BaseModel):

    model_name: str
    model_version: str
    trained_at: datetime
    target_column: str
    feature_columns: list[str]
    metrics: dict[str, float]
    decision_threshold: float
    dataset_name: str
    dataset_version: str | None = None
