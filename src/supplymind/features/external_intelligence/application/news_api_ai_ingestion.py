"""NewsAPI.ai ingestion: fetch, normalize, deduplicate, geocode and persist."""

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
from supplymind.features.external_intelligence.infrastructure.news_api_ai import (
    NewsApiAiClient,
)
from supplymind.features.external_intelligence.infrastructure.open_meteo import (
    OpenMeteoClient,
)


class IngestNewsApiAiEvents:
    """Normalize NewsAPI.ai articles into SupplyMind event-domain records."""

    def __init__(
        self,
        *,
        news_client: NewsApiAiClient,
        extractor: StructuredEventExtractor,
        geocoder: OpenMeteoClient,
        upsert_event: UpsertEvent,
    ) -> None:
        self.news_client = news_client
        self.extractor = extractor
        self.geocoder = geocoder
        self.upsert_event = upsert_event

    async def execute(self) -> list[SupplyChainEvent]:
        articles = await self.news_client.fetch_recent()
        if not articles:
            return []

        extractions = await self.extractor.extract_many(articles)
        candidates: list[EventCandidate] = []

        for article, extracted in zip(articles, extractions, strict=True):
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

        candidates = deduplicate_events(candidates)
        persisted: list[SupplyChainEvent] = []

        for candidate in candidates:
            latitude = None
            longitude = None
            location_query = candidate.city or candidate.region

            if location_query:
                try:
                    resolved = await self.geocoder.geocode(location_query)
                    if resolved is not None:
                        latitude = resolved.latitude
                        longitude = resolved.longitude
                except Exception as exc:
                    print(
                        "NewsAPI.ai event geocoding skipped for "
                        f"'{candidate.title}': {exc}"
                    )

            external_id = hashlib.sha256(
                candidate.source_url.encode("utf-8")
            ).hexdigest()

            event = await self.upsert_event.execute(
                external_id=external_id,
                source="newsapi_ai",
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
                    "provider": "NewsAPI.ai",
                    "article_url": candidate.source_url,
                    "original_title": candidate.original_title,
                    "source_language": candidate.source_language,
                    "domain": candidate.domain,
                    "normalized_title": candidate.title,
                },
            )
            persisted.append(event)

        return persisted
