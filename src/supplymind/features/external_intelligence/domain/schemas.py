"""External-intelligence domain schemas."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


# -------------------
# Location
# -------------------

class ResolvedLocation(BaseModel):
    """Geocoded location used for weather and event context."""

    name: str
    country: str | None = None
    country_code: str | None = None
    region: str | None = None
    latitude: float
    longitude: float
    timezone: str | None = None


# -------------------
# Weather
# -------------------

class WeatherRiskAssessment(BaseModel):
    """Deterministic weather-risk summary for a shipment location."""

    location: ResolvedLocation
    risk_level: str
    risk_score: float = Field(ge=0.0, le=1.0)
    max_precipitation_probability: float | None = None
    max_wind_gust_kmh: float | None = None
    total_precipitation_mm: float | None = None
    total_snowfall_cm: float | None = None
    minimum_visibility_m: float | None = None
    reasons: list[str] = Field(default_factory=list)
    forecast_start: datetime | None = None
    forecast_end: datetime | None = None


# -------------------
# GDELT source article
# -------------------

class GdeltArticle(BaseModel):
    """Small stable projection of a GDELT DOC article."""

    url: str
    title: str
    domain: str | None = None
    source_country: str | None = None
    language: str | None = None
    seen_at: datetime | None = None


# -------------------
# Event taxonomy
# -------------------

class EventType(StrEnum):
    """Controlled SupplyMind V1 disruption taxonomy."""

    SEVERE_WEATHER = "severe_weather"
    FLOODING = "flooding"
    STRIKE = "strike"
    PORT_CONGESTION = "port_congestion"
    GEOPOLITICAL = "geopolitical"
    BORDER_CLOSURE = "border_closure"
    FACTORY_INCIDENT = "factory_incident"
    TRANSPORT_INTERRUPTION = "transport_interruption"
    PUBLIC_HEALTH = "public_health"
    PLANNED_EVENT = "planned_event"
    OTHER = "other"


# -------------------
# Structured event extraction
# -------------------

class ExtractedSupplyChainEvent(BaseModel):
    """Validated event extracted from a candidate GDELT article.

    All application-facing text is normalized to English. Original source
    language/title/url remain available on ``GdeltArticle`` and are persisted
    in the event ``raw_payload`` for provenance.
    """

    is_relevant: bool = Field(
        description=(
            "True only for a concrete operational disruption that could "
            "plausibly affect movement of goods, transport capacity, "
            "production supply, border flow, ports, warehousing or delivery."
        )
    )

    event_type: EventType = EventType.OTHER

    normalized_title: str | None = Field(
        default=None,
        description="Short English title describing the disruption.",
    )

    summary: str | None = Field(
        default=None,
        description=(
            "Concise English operational summary grounded only in the "
            "provided article metadata."
        ),
    )

    severity: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description=(
            "Operational severity from 0 to 1. "
            "0.0-0.2 minimal, 0.3-0.4 low/local, "
            "0.5-0.6 moderate, 0.7-0.8 major, "
            "0.9-1.0 critical/widespread."
        ),
    )

    country: str | None = Field(
        default=None,
        description="Country name normalized to English.",
    )
    region: str | None = Field(
        default=None,
        description="Region/state/province normalized to English.",
    )
    city: str | None = Field(
        default=None,
        description="City normalized to English when supported.",
    )

    starts_at: datetime | None = None
    ends_at: datetime | None = None

    rationale: str | None = Field(
        default=None,
        description=(
            "Brief explanation of why the article is or is not considered "
            "an operational supply-chain disruption."
        ),
    )
