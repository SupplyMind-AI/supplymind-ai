"""Async NewsAPI.ai (Event Registry) article client.

The client uses the documented REST article-search endpoint instead of the Python
SDK so deployment stays lightweight and deterministic.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from supplymind.features.external_intelligence.domain.schemas import NewsArticle


class NewsApiAiError(RuntimeError):
    """Controlled provider failure suitable for graceful API degradation."""


def _parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None


def _source_country(source: dict[str, Any]) -> str | None:
    location = source.get("location") or {}
    if isinstance(location, dict):
        return (
            location.get("country")
            or location.get("label")
            or location.get("countryCode")
        )
    return None


class NewsApiAiClient:
    """Fetch recent disruption-focused articles from NewsAPI.ai."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str,
        query: str,
        language: str = "eng",
        lookback_days: int = 3,
        max_records: int = 40,
        timeout_seconds: float = 20.0,
        max_retries: int = 3,
        retry_wait_seconds: float = 2.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.query = query
        self.language = language
        self.lookback_days = max(1, min(lookback_days, 30))
        self.max_records = max(1, min(max_records, 100))
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(1, max_retries)
        self.retry_wait_seconds = max(0.5, retry_wait_seconds)

    async def fetch_recent(self) -> list[NewsArticle]:
        if not self.api_key:
            raise NewsApiAiError(
                "NEWS_API_AI_API_KEY is not configured. Existing stored events remain available."
            )

        today = datetime.now(timezone.utc).date()
        start = today - timedelta(days=self.lookback_days)

        body = {
            "action": "getArticles",
            "keyword": self.query,
            "keywordSearchMode": "exact",
            "keywordLoc": "body,title",
            "lang": self.language,
            "dateStart": start.isoformat(),
            "dateEnd": today.isoformat(),
            "articlesPage": 1,
            "articlesCount": self.max_records,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "resultType": "articles",
            "includeArticleTitle": True,
            "includeArticleBasicInfo": True,
            "includeArticleBody": True,
            "infoArticleBodyLen": 900,
            "includeArticleLocation": True,
            "includeSourceTitle": True,
            "includeSourceLocation": True,
            "apiKey": self.api_key,
        }

        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            for attempt in range(1, self.max_retries + 1):
                try:
                    response = await client.post(
                        self.base_url,
                        json=body,
                        headers={"Content-Type": "application/json"},
                    )
                except (httpx.TimeoutException, httpx.NetworkError) as exc:
                    if attempt >= self.max_retries:
                        raise NewsApiAiError(
                            f"NewsAPI.ai network request failed after {attempt} attempts."
                        ) from exc
                    await asyncio.sleep(self.retry_wait_seconds * attempt)
                    continue

                if response.status_code == 204:
                    return []

                if response.status_code in {401, 403}:
                    raise NewsApiAiError(
                        "NewsAPI.ai rejected the API key or the account has no remaining access."
                    )

                if response.status_code == 429:
                    if attempt >= self.max_retries:
                        raise NewsApiAiError(
                            "NewsAPI.ai rate limit remained active after retries."
                        )
                    wait = self.retry_wait_seconds * attempt
                    retry_after = response.headers.get("Retry-After")
                    if retry_after:
                        try:
                            wait = max(wait, float(retry_after))
                        except ValueError:
                            pass
                    await asyncio.sleep(wait)
                    continue

                if response.status_code >= 500:
                    if attempt >= self.max_retries:
                        raise NewsApiAiError(
                            f"NewsAPI.ai service unavailable ({response.status_code})."
                        )
                    await asyncio.sleep(self.retry_wait_seconds * attempt)
                    continue

                if response.status_code >= 400:
                    detail = response.text[:300]
                    raise NewsApiAiError(
                        f"NewsAPI.ai request rejected ({response.status_code}): {detail}"
                    )

                try:
                    payload = response.json()
                except ValueError as exc:
                    raise NewsApiAiError("NewsAPI.ai returned invalid JSON.") from exc

                results = ((payload.get("articles") or {}).get("results") or [])
                articles: list[NewsArticle] = []

                for item in results:
                    if not isinstance(item, dict):
                        continue
                    url = item.get("url")
                    title = item.get("title")
                    if not url or not title:
                        continue

                    source = item.get("source") or {}
                    if not isinstance(source, dict):
                        source = {}
                    location = item.get("location") or {}
                    if not isinstance(location, dict):
                        location = {}

                    body_text = str(item.get("body") or "").strip()
                    articles.append(
                        NewsArticle(
                            url=str(url),
                            title=str(title),
                            domain=str(source.get("uri") or "") or None,
                            source_title=str(source.get("title") or "") or None,
                            source_country=_source_country(source),
                            language=str(item.get("lang") or "") or None,
                            seen_at=_parse_datetime(
                                item.get("dateTime") or item.get("date")
                            ),
                            body_excerpt=body_text[:900] or None,
                            location_name=str(location.get("label") or "") or None,
                        )
                    )

                return articles

        return []
