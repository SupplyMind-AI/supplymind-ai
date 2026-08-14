"""LLM structured extraction for provider-neutral supply-chain news."""

from __future__ import annotations

import asyncio

from langchain_openai import ChatOpenAI

from supplymind.features.external_intelligence.domain.schemas import (
    ExtractedSupplyChainEvent,
    NewsArticle,
)


_SYSTEM_PROMPT = """
You are the SupplyMind external-event extraction component.

Your job is NOT to summarize every logistics-related article.
Your job is to decide whether the article describes a concrete operational
disruption that could plausibly affect shipments or supply-chain operations.

RELEVANCE GATE

Set is_relevant=true only when there is a concrete disruption such as:
- severe weather affecting transport or logistics
- flooding
- labor strike
- port congestion or closure
- geopolitical conflict affecting transport/trade
- border closure or customs interruption
- factory/industrial incident causing supply interruption
- rail, road, air, maritime or cargo transport interruption
- major public-health restriction affecting logistics
- a planned event with a credible operational logistics impact

Set is_relevant=false for:
- investments, loans or financing
- infrastructure approvals or future construction
- policy announcements without an active disruption
- assistance schemes
- company promotions or ordinary business news
- throughput growth or positive operational milestones
- general logistics commentary
- announcements with no concrete current/planned operational impact

CONTROLLED EVENT TAXONOMY

Pick exactly one:
severe_weather
flooding
strike
port_congestion
geopolitical
border_closure
factory_incident
transport_interruption
public_health
planned_event
other

Use "other" only for a real disruption that does not fit another category.
Do not invent new event type labels.

SEVERITY RUBRIC

0.0-0.2 = minimal/informational operational effect
0.3-0.4 = low or localized disruption
0.5-0.6 = moderate disruption affecting a route, terminal, port, facility or region
0.7-0.8 = major disruption with substantial capacity loss, shutdown, flooding,
          attack, cancellation or regional interruption
0.9-1.0 = critical/widespread disruption affecting a major corridor, large port,
          multiple regions or causing broad operational shutdown

Do not assign high severity just because an article sounds important.
Severity measures operational disruption, not news importance.

LANGUAGE

Return normalized_title, summary, country, region and city in ENGLISH,
regardless of the source language.

GROUNDING

Use only the supplied article metadata/body excerpt.
Do not invent locations, dates, severity evidence, causes or impacts.
If a field is unsupported, return null.
"""


class StructuredEventExtractor:
    """Provider-backed extractor with validated structured output."""

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
        max_concurrency: int = 4,
    ) -> None:
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be at least 1.")

        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0,
        )

        self.structured_llm = llm.with_structured_output(
            ExtractedSupplyChainEvent,
            method="json_schema",
        )
        self._semaphore = asyncio.Semaphore(max_concurrency)

    async def extract(
        self,
        article: NewsArticle,
    ) -> ExtractedSupplyChainEvent:
        """Extract one normalized disruption event."""

        prompt = (
            f"{_SYSTEM_PROMPT}\n\n"
            "ARTICLE METADATA\n"
            f"Original title: {article.title}\n"
            f"Source: {article.source_title or article.domain or 'unknown'}\n"
            f"Source language: {article.language or 'unknown'}\n"
            f"Domain: {article.domain or 'unknown'}\n"
            f"Source country: {article.source_country or 'unknown'}\n"
            f"Provider location: {article.location_name or 'unknown'}\n"
            f"Published at: {article.seen_at or 'unknown'}\n"
            f"Body excerpt: {article.body_excerpt or 'not provided'}\n"
            f"URL: {article.url}"
        )

        async with self._semaphore:
            result = await self.structured_llm.ainvoke(prompt)

        return result

    async def extract_many(
        self,
        articles: list[NewsArticle],
    ) -> list[ExtractedSupplyChainEvent | None]:
        """Extract several articles with bounded concurrency."""

        async def safe_extract(
            article: NewsArticle,
        ) -> ExtractedSupplyChainEvent | None:
            try:
                return await self.extract(article)
            except Exception as exc:
                print(
                    "Event extraction skipped article "
                    f"'{article.title[:80]}': {exc}"
                )
                return None

        return await asyncio.gather(
            *(safe_extract(article) for article in articles)
        )
