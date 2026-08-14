from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from apps.api.dependencies import (
    get_event_repository,
    get_news_api_ai_client,
    get_open_meteo_client,
    get_settings_dependency,
)
from supplymind.features.events.application.use_cases import UpsertEvent
from supplymind.features.external_intelligence.application.news_api_ai_ingestion import (
    IngestNewsApiAiEvents,
)
from supplymind.features.external_intelligence.infrastructure.event_extractor import (
    StructuredEventExtractor,
)
from supplymind.features.external_intelligence.infrastructure.news_api_ai import (
    NewsApiAiError,
)

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def list_items(
    limit: int = Query(100, ge=1, le=200),
    event_type: str | None = None,
    country: str | None = None,
    min_severity: float | None = Query(None, ge=0, le=1),
    repo=Depends(get_event_repository),
):
    rows = await repo.list_active(at=datetime.now(timezone.utc), limit=limit)
    result = []
    for event in rows:
        if event_type and event.event_type != event_type:
            continue
        if country and (event.country or "").casefold() != country.casefold():
            continue
        if min_severity is not None and (event.severity or 0) < min_severity:
            continue
        result.append(
            {
                "id": str(event.id),
                "source": event.source,
                "event_type": event.event_type,
                "title": event.title,
                "description": event.description,
                "severity": event.severity,
                "country": event.country,
                "region": event.region,
                "latitude": event.latitude,
                "longitude": event.longitude,
                "starts_at": event.starts_at.isoformat() if event.starts_at else None,
                "created_at": event.created_at.isoformat() if event.created_at else None,
            }
        )
    return result


@router.post("/refresh")
async def refresh(
    repo=Depends(get_event_repository),
    cfg=Depends(get_settings_dependency),
):
    use_case = IngestNewsApiAiEvents(
        news_client=get_news_api_ai_client(),
        extractor=StructuredEventExtractor(
            model=cfg.llm_model,
            api_key=cfg.openai_api_key,
        ),
        geocoder=get_open_meteo_client(),
        upsert_event=UpsertEvent(repo),
    )

    try:
        items = await use_case.execute()
        return {
            "status": "ok",
            "provider": "NewsAPI.ai",
            "ingested": len(items),
            "message": f"Refreshed {len(items)} normalized supply-chain events.",
        }
    except NewsApiAiError as exc:
        return {
            "status": "degraded",
            "provider": "NewsAPI.ai",
            "ingested": 0,
            "message": str(exc),
            "using_stored_events": True,
        }
    except Exception as exc:
        print(f"NewsAPI.ai refresh degraded: {type(exc).__name__}: {exc}")
        return {
            "status": "degraded",
            "provider": "NewsAPI.ai",
            "ingested": 0,
            "message": "External refresh is temporarily unavailable. Stored events remain available.",
            "using_stored_events": True,
        }
