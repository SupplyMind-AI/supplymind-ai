"""GDELT ingestion use case with relevance filtering and deduplication."""

from __future__ import annotations

import hashlib

from supplymind.features.events.application.use_cases import UpsertEvent
from supplymind.features.events.domain.entities import SupplyChainEvent
from supplymind.features.external_intelligence.application.event_deduplication import (
    EventCandidate,
    deduplicate_events,
)
from supplymind.features.external_intelligence.infrastructure.event_extractor import (
    StructuredEventExtractor,
)
from supplymind.features.external_intelligence.infrastructure.gdelt import GdeltClient
from supplymind.features.external_intelligence.infrastructure.open_meteo import (
    OpenMeteoClient,
)


class IngestGdeltEvents:
    """Fetch, extract, normalize, deduplicate, geocode, and persist GDELT events."""

    def __init__(
        self,
        *,
        gdelt_client: GdeltClient,
        extractor: StructuredEventExtractor,
        geocoder: OpenMeteoClient,
        upsert_event: UpsertEvent,
    ) -> None:
        self.gdelt_client = gdelt_client
        self.extractor = extractor
        self.geocoder = geocoder
        self.upsert_event = upsert_event

    async def execute(self) -> list[SupplyChainEvent]:
        articles = await self.gdelt_client.fetch_recent()

        if not articles:
            return []

        extractions = await self.extractor.extract_many(articles)

        candidates: list[EventCandidate] = []

        # -------------------
        # Relevance gate + canonicalization
        # -------------------

        for article, extracted in zip(
            articles,
            extractions,
            strict=True,
        ):
            if extracted is None or not extracted.is_relevant:
                continue

            if not extracted.normalized_title:
                continue

            candidates.append(
                EventCandidate(
                    source_url=article.url,
                    event_type=extracted.event_type,
                    title=extracted.normalized_title,
                    summary=extracted.summary,
                    severity=float(extracted.severity or 0.3),
                    country=extracted.country or article.source_country,
                    region=extracted.region,
                    city=extracted.city,
                    published_at=extracted.starts_at or article.seen_at,
                    original_title=article.title,
                    source_language=article.language,
                    domain=article.domain,
                )
            )

        # -------------------
        # Deterministic deduplication
        # -------------------

        candidates = deduplicate_events(candidates)

        persisted: list[SupplyChainEvent] = []

        # -------------------
        # Geocoding + persistence
        # -------------------

        for candidate in candidates:
            latitude = None
            longitude = None

            # Prefer the most specific supported location.
            # We intentionally do NOT fall back to a country centroid because
            # that would imply false geographic precision on the Event Monitor.
            location_query = (
                candidate.city
                or candidate.region
            )

            if location_query:
                try:
                    resolved = await self.geocoder.geocode(
                        location_query,
                    )
                    if resolved is not None:
                        latitude = resolved.latitude
                        longitude = resolved.longitude
                except Exception as exc:
                    print(
                        "Geocoding skipped for "
                        f"'{candidate.title}': {exc}"
                    )

            external_id = hashlib.sha256(
                candidate.source_url.encode("utf-8")
            ).hexdigest()

            event = await self.upsert_event.execute(
                external_id=external_id,
                source="gdelt",
                event_type=candidate.event_type.value,
                title=candidate.title,
                description=candidate.summary,
                severity=candidate.severity,
                country=candidate.country,
                region=candidate.region,
                latitude=latitude,
                longitude=longitude,
                starts_at=candidate.published_at,
                ends_at=None,
                raw_payload={
                    "article_url": candidate.source_url,
                    "original_title": candidate.original_title,
                    "source_language": candidate.source_language,
                    "domain": candidate.domain,
                    "normalized_title": candidate.title,
                },
            )
            persisted.append(event)

        return persisted
