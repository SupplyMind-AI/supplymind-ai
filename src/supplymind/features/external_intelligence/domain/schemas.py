"""External-intelligence domain schemas."""
from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class ResolvedLocation(BaseModel):
    name: str
    country: str | None = None
    country_code: str | None = None
    region: str | None = None
    latitude: float
    longitude: float
    timezone: str | None = None

class WeatherRiskAssessment(BaseModel):
    location: ResolvedLocation
    risk_level: str
    risk_score: float = Field(ge=0.0, le=1.0)
    max_precipitation_probability: float | None = None
    max_wind_gust_kmh: float | None = None
    total_precipitation_mm: float | None = None
    total_snowfall_cm: float | None = None
    minimum_visibility_m: float | None = None
    reasons: list[str] = []
    forecast_start: datetime | None = None
    forecast_end: datetime | None = None

class GdeltArticle(BaseModel):
    url: str
    title: str
    domain: str | None = None
    source_country: str | None = None
    language: str | None = None
    seen_at: datetime | None = None

class ExtractedSupplyChainEvent(BaseModel):
    relevant: bool
    event_type: str | None = None
    title: str | None = None
    description: str | None = None
    severity: float | None = Field(default=None, ge=0.0, le=1.0)
    country: str | None = None
    region: str | None = None
    city: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    rationale: str | None = None
