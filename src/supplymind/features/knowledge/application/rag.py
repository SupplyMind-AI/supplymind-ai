"""Grounded RAG answer generation over enterprise knowledge."""

from __future__ import annotations

import json

from langchain_openai import ChatOpenAI


class GroundedRag:
    """Retrieve enterprise chunks and synthesize a citation-backed answer."""

    def __init__(
        self,
        *,
        semantic_search,
        model: str,
        api_key: str | None,
    ) -> None:
        self.semantic_search = semantic_search
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0,
        )

    async def execute(self, query: str, *, top_k: int = 5) -> dict:
        query = query.strip()
        if not query:
            return {
                "answer": "Please enter a question.",
                "evidence": [],
                "grounded": False,
            }

        hits = await self.semantic_search.execute(
            query,
            top_k=min(max(top_k, 1), 10),
        )

        evidence = [
            {
                "id": hit.id,
                "score": hit.score,
                "text": hit.text,
                "metadata": hit.metadata,
            }
            for hit in hits
        ]

        if not evidence:
            return {
                "answer": (
                    "I could not find relevant enterprise evidence for this question. "
                    "Try a more specific policy, SLA, refund, payment or operational query."
                ),
                "evidence": [],
                "grounded": False,
            }

        context = [
            {
                "source_id": item["id"],
                "score": item["score"],
                "metadata": item["metadata"],
                "text": item["text"],
            }
            for item in evidence
        ]

        prompt = (
            "You are SupplyMind RAG. Answer ONLY from the provided enterprise "
            "knowledge chunks. Do not invent policy details. If the chunks are "
            "insufficient, say so. Keep the answer operational and concise. "
            "Reference source IDs in square brackets when making supported claims.\n\n"
            f"QUESTION:\n{query}\n\n"
            f"RETRIEVED EVIDENCE JSON:\n{json.dumps(context, default=str)}"
        )

        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content
            if isinstance(content, str):
                answer = content
            else:
                answer = str(content)
        except Exception as exc:
            return {
                "answer": (
                    "Answer generation is temporarily unavailable, but the retrieved "
                    "enterprise evidence is shown below."
                ),
                "evidence": evidence,
                "grounded": True,
                "generation_degraded": True,
                "generation_error": str(exc),
            }

        return {
            "answer": answer,
            "evidence": evidence,
            "grounded": True,
            "retrieved": len(evidence),
        }
