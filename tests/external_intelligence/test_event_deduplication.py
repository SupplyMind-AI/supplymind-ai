from datetime import datetime, timezone

from supplymind.features.external_intelligence.application.event_deduplication import (
    EventCandidate,
    deduplicate_events,
)
from supplymind.features.external_intelligence.domain.schemas import EventType


def _candidate(
    *,
    url: str,
    title: str,
    severity: float,
    region: str | None,
) -> EventCandidate:
    return EventCandidate(
        source_url=url,
        event_type=EventType.PORT_CONGESTION,
        title=title,
        summary="Operational disruption.",
        severity=severity,
        country="India",
        region=region,
        city=None,
        published_at=datetime(
            2026,
            8,
            12,
            10,
            tzinfo=timezone.utc,
        ),
        original_title=title,
        source_language="English",
        domain="example.com",
    )


def test_same_url_is_deduplicated():
    events = deduplicate_events(
        [
            _candidate(
                url="https://example.com/story",
                title="Visakhapatnam Port congestion disrupts cargo",
                severity=0.4,
                region=None,
            ),
            _candidate(
                url="https://example.com/story",
                title="Visakhapatnam Port congestion disrupts cargo",
                severity=0.6,
                region="Andhra Pradesh",
            ),
        ]
    )

    assert len(events) == 1
    assert events[0].severity == 0.6
    assert events[0].region == "Andhra Pradesh"


def test_different_real_events_are_preserved():
    events = deduplicate_events(
        [
            _candidate(
                url="https://a.example/story",
                title="Jeddah Port congestion disrupts cargo flows",
                severity=0.6,
                region="Jeddah",
            ),
            _candidate(
                url="https://b.example/story",
                title="Mumbai Port congestion disrupts cargo flows",
                severity=0.6,
                region="Maharashtra",
            ),
        ]
    )

    assert len(events) == 2
