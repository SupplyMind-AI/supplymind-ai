"""Deterministic within-batch event deduplication."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher

from supplymind.features.external_intelligence.domain.schemas import EventType


# -------------------
# Candidate
# -------------------

@dataclass
class EventCandidate:
    """Normalized event candidate before persistence."""

    source_url: str
    event_type: EventType
    title: str
    summary: str | None
    severity: float
    country: str | None
    region: str | None
    city: str | None
    published_at: datetime | None
    original_title: str
    source_language: str | None
    domain: str | None


# -------------------
# Normalization
# -------------------

def _normalize_title(value: str) -> str:
    """Normalize the English title for deterministic comparison."""

    lowered = value.casefold()
    without_symbols = re.sub(r"[^a-z0-9\s]", " ", lowered)
    return " ".join(without_symbols.split())


def _title_similarity(left: str, right: str) -> float:
    return SequenceMatcher(
        None,
        _normalize_title(left),
        _normalize_title(right),
    ).ratio()


def _compatible_location(
    left: EventCandidate,
    right: EventCandidate,
) -> bool:
    """Check whether two candidates describe a compatible location."""

    left_country = _normalize_location(
        left.country
    )
    right_country = _normalize_location(
        right.country
    )

    if (
        left_country
        and right_country
        and left_country != right_country
    ):
        return False

    left_region = _normalize_location(
        left.region
    )
    right_region = _normalize_location(
        right.region
    )

    if (
        left_region
        and right_region
    ):
        return left_region == right_region

    return True


def _as_utc(value: datetime | None) -> datetime | None:
    """Normalize a datetime to timezone-aware UTC."""

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def _within_window(
    left: datetime | None,
    right: datetime | None,
    *,
    window: timedelta,
) -> bool:
    """Check whether two event timestamps fall within the dedup window."""

    left_utc = _as_utc(left)
    right_utc = _as_utc(right)

    if left_utc is None or right_utc is None:
        return True

    return abs(left_utc - right_utc) <= window


def _normalize_location(value: str | None) -> str | None:
    """Normalize a country/region label for deterministic comparison."""

    if not value:
        return None

    normalized = value.casefold()

    normalized = re.sub(
        r"\b(and|the)\b",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"[^a-z0-9\s]",
        " ",
        normalized,
    )

    return " ".join(
        sorted(normalized.split())
    )

# -------------------
# Deduplication
# -------------------

def deduplicate_events(
    candidates: list[EventCandidate],
    *,
    title_similarity_threshold: float = 0.88,
    publication_window_hours: int = 48,
) -> list[EventCandidate]:
    """Collapse duplicate disruption candidates.

    Exact source URLs are duplicates immediately.

    Cross-source stories are considered duplicates only when event type,
    compatible location, publication time and normalized English titles align.
    """

    unique: list[EventCandidate] = []
    window = timedelta(hours=publication_window_hours)

    for candidate in candidates:
        duplicate_index: int | None = None

        for index, existing in enumerate(unique):
            same_url = (
                candidate.source_url
                and candidate.source_url == existing.source_url
            )

            same_event = (
                candidate.event_type == existing.event_type
                and _compatible_location(candidate, existing)
                and _within_window(
                    candidate.published_at,
                    existing.published_at,
                    window=window,
                )
                and _title_similarity(
                    candidate.title,
                    existing.title,
                ) >= title_similarity_threshold
            )

            if same_url or same_event:
                duplicate_index = index
                break

        if duplicate_index is None:
            unique.append(candidate)
            continue

        existing = unique[duplicate_index]

        # Keep the more severe candidate while filling missing location fields
        # from the other record. This is deterministic and does not re-call the LLM.
        winner = (
            candidate
            if candidate.severity > existing.severity
            else existing
        )
        loser = existing if winner is candidate else candidate

        winner.region = winner.region or loser.region
        winner.city = winner.city or loser.city
        winner.country = winner.country or loser.country
        winner.summary = winner.summary or loser.summary

        unique[duplicate_index] = winner

    return unique
