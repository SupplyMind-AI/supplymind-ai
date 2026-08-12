"""GDELT DOC 2.0 client."""
import asyncio
from datetime import datetime

import httpx

from supplymind.features.external_intelligence.domain.schemas import (
    GdeltArticle,
)

from datetime import datetime


def _parse_seen_at(value: str | None) -> datetime | None:
    """Parse a GDELT seendate value."""

    if not value:
        return None

    try:
        return datetime.strptime(
            value,
            "%Y%m%dT%H%M%SZ",
        )
    except ValueError:
        return None


class GdeltClient:
    """Fetch recent supply-chain-related articles from GDELT DOC 2.0."""

    def __init__(
        self,
        *,
        base_url: str,
        query: str,
        timespan: str = "24h",
        max_records: int = 50,
        timeout_seconds: float = 20.0,
        max_retries: int = 4,
    ) -> None:
        self.base_url = base_url
        self.query = query
        self.timespan = timespan
        self.max_records = max_records
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    async def fetch_recent(self) -> list[GdeltArticle]:
        params = {
            "query": self.query,
            "mode": "ArtList",
            "format": "json",
            "sort": "HybridRel",
            "timespan": self.timespan,
            "maxrecords": self.max_records,
        }

        async with httpx.AsyncClient(
            timeout=self.timeout_seconds
        ) as client:

            for attempt in range(self.max_retries):
                response = await client.get(
                    self.base_url,
                    params=params,
                )

                if response.status_code == 429:
                    retry_after = response.headers.get(
                        "Retry-After"
                    )

                    wait_seconds = (
                        float(retry_after)
                        if retry_after
                        else 2 ** attempt
                    )

                    print(
                        "GDELT rate limit reached. "
                        f"Retrying in {wait_seconds:.0f}s..."
                    )

                    await asyncio.sleep(wait_seconds)
                    continue

                response.raise_for_status()

                payload = response.json()

                return [
                    GdeltArticle(
                        url=item["url"],
                        title=item["title"],
                        domain=item.get("domain"),
                        source_country=item.get(
                            "sourcecountry"
                        ),
                        language=item.get("language"),
                        seen_at=_parse_seen_at(
                            item.get("seendate")
                        ),
                    )
                    for item in payload.get(
                        "articles",
                        [],
                    )
                    if item.get("url")
                    and item.get("title")
                ]

        raise RuntimeError(
            "GDELT request failed after "
            f"{self.max_retries} retries due to rate limiting."
        )