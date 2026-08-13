from __future__ import annotations
from pydantic import BaseModel, Field


class RiskDistribution(BaseModel):
    low: int = 0
    medium: int = 0
    high: int = 0


class DashboardPrediction(BaseModel):
    external_id: str
    destination: str | None = None
    delayed: bool
    delay_probability: float
    threshold: float
    risk_level: str
    explanation: str
    created_at: str | None = None


class DashboardEvent(BaseModel):
    id: str
    title: str
    event_type: str
    severity: float | None = None
    country: str | None = None
    region: str | None = None


class DashboardSummary(BaseModel):
    shipment_count: int
    prediction_count: int
    delayed_prediction_rate: float
    average_delay_probability: float
    active_event_count: int
    queued_retraining_jobs: int
    champion_model_name: str | None = None
    champion_model_version: str | None = None
    champion_threshold: float | None = None
    risk_distribution: RiskDistribution = Field(default_factory=RiskDistribution)
    recent_predictions: list[DashboardPrediction] = Field(default_factory=list)
    recent_events: list[DashboardEvent] = Field(default_factory=list)
