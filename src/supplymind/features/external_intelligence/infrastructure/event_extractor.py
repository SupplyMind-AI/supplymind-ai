"""Structured LLM extraction for GDELT article metadata."""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from supplymind.features.external_intelligence.domain.schemas import (
    ExtractedSupplyChainEvent,
    GdeltArticle,
)

SYSTEM_PROMPT = """
You extract supply-chain disruption events from news metadata.

Mark an item relevant only when it describes a concrete event that could plausibly
impact logistics, transportation, ports, warehousing, manufacturing supply, or delivery.
Never invent locations, dates, severity, or causal effects. If a field is unsupported,
return null. Treat severity as an operational-impact estimate grounded only in the input.
"""


class StructuredEventExtractor:
    """Extract a validated event schema from one GDELT article."""

    def __init__(
        self,
        *,
        model: str,
        api_key: str | None = None,
    ) -> None:
        llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0,
        )
        self.structured_llm = llm.with_structured_output(
            ExtractedSupplyChainEvent,
            method="json_schema",
        )

    async def extract(
        self,
        article: GdeltArticle,
    ) -> ExtractedSupplyChainEvent:
        prompt = f"""{SYSTEM_PROMPT}

Title: {article.title}
Domain: {article.domain or 'unknown'}
Source country: {article.source_country or 'unknown'}
Seen at: {article.seen_at or 'unknown'}
URL: {article.url}
"""
        return await self.structured_llm.ainvoke(prompt)
