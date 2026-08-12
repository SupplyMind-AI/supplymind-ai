"""GDELT DOC 2.0 client with rate-limit-safe retries."""

from __future__ import annotations

import asyncio
from datetime import datetime

import httpx

from supplymind.features.external_intelligence.domain.schemas import GdeltArticle


# -------------------
# Disruption-focused query
# -------------------

DEFAULT_DISRUPTION_QUERY = (
    "("
    "\"port congestion\" OR "
    "\"port closure\" OR "
    "\"shipping disruption\" OR "
    "\"freight disruption\" OR "
    "\"cargo disruption\" OR "
    "\"logistics disruption\" OR "
    "\"border closure\" OR "
    "\"rail disruption\" OR "
    "\"transport strike\" OR "
    "\"port strike\" OR "
    "blockade OR flooding OR typhoon OR wildfire"
    ")"
)


# -------------------
# Date parsing
# -------------------

def _parse_seen_at(value: str | None) -> datetime | None:
    """Parse common GDELT seendate formats."""

    if not value:
        return None

    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


# -------------------
# GDELT client
# -------------------

class GdeltClient:
    """Fetch recent disruption candidates from GDELT DOC 2.0."""

    def __init__(
        self,
        *,
        base_url: str,
        query: str | None = None,
        timespan: str = "24h",
        max_records: int = 50,
        timeout_seconds: float = 15.0,
        max_retries: int = 4,
        retry_wait_seconds: float = 5.0,
    ) -> None:
        self.base_url = base_url
        self.query = query or DEFAULT_DISRUPTION_QUERY
        self.timespan = timespan
        self.max_records = max_records
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_wait_seconds = max(retry_wait_seconds, 5.0)

    async def fetch_recent(self) -> list[GdeltArticle]:
        """Fetch recent article candidates with conservative retry behavior."""

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
            for attempt in range(1, self.max_retries + 1):
                print(
                    f"GDELT request attempt "
                    f"{attempt}/{self.max_retries}..."
                )

                try:
                    response = await client.get(
                        self.base_url,
                        params=params,
                    )
                except httpx.TimeoutException:
                    if attempt == self.max_retries:
                        raise RuntimeError(
                            "GDELT request timed out after "
                            f"{self.max_retries} attempts."
                        )

                    print(
                        "GDELT request timed out. "
                        f"Retrying in {self.retry_wait_seconds:.0f}s..."
                    )
                    await asyncio.sleep(self.retry_wait_seconds)
                    continue

                if response.status_code == 429:
                    if attempt == self.max_retries:
                        raise RuntimeError(
                            "GDELT rate limit remained active after "
                            f"{self.max_retries} attempts."
                        )

                    retry_after = response.headers.get("Retry-After")
                    wait_seconds = self.retry_wait_seconds

                    if retry_after:
                        try:
                            wait_seconds = max(
                                float(retry_after),
                                self.retry_wait_seconds,
                            )
                        except ValueError:
                            pass

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
                        source_country=item.get("sourcecountry"),
                        language=item.get("language"),
                        seen_at=_parse_seen_at(item.get("seendate")),
                    )
                    for item in payload.get("articles", [])
                    if item.get("url") and item.get("title")
                ]

        return []
