"""Progress-aware SupplyMind assistant execution for a responsive UI."""
from __future__ import annotations
import asyncio, json, time
from typing import AsyncIterator
from langchain_openai import ChatOpenAI
from langsmith import traceable
from supplymind.features.assistant.application.routing import route_query
from supplymind.features.assistant.domain.schemas import AssistantAnswer, AssistantRequest

SYSTEM = """You are the SupplyMind operational assistant. Answer only from supplied context. Never invent shipment facts, model outputs, weather, events, document content or causal explanations. A model prediction is a risk estimate, not proof of cause. Weather/events are external context only unless a route match is explicitly present. If evidence is insufficient, say what is missing. Cite only supplied source IDs. Be concise and operational."""


class SupplyMindStreamingAssistant:
    def __init__(self, *, tools: dict, model: str, api_key: str | None = None) -> None:
        self.tools = tools
        llm = ChatOpenAI(model=model, api_key=api_key, temperature=0)
        self.answer_llm = llm.with_structured_output(AssistantAnswer, method="json_schema")

    async def _run_timed(self, key: str, coro):
        started = time.perf_counter()
        try:
            value = await coro
            return key, value, time.perf_counter() - started, None
        except Exception as exc:
            return key, None, time.perf_counter() - started, str(exc)

    @traceable(name="supplymind-assistant-stream")
    async def stream(self, request: AssistantRequest) -> AsyncIterator[dict]:
        total_started = time.perf_counter()
        yield {"type": "progress", "stage": "start", "label": "Understanding your question", "status": "running", "elapsed": 0.0}
        intent = route_query(request.query, shipment_external_id=request.shipment_external_id, location=request.location)
        yield {"type": "progress", "stage": "route", "label": f"Route selected: {intent}", "status": "done", "elapsed": time.perf_counter()-total_started}

        context: list[dict] = []
        location = request.location

        if request.shipment_external_id:
            started = time.perf_counter()
            yield {"type": "progress", "stage": "shipment", "label": "Looking up shipment and latest prediction", "status": "running", "elapsed": time.perf_counter()-total_started}
            shipment = await self.tools["shipment_context"].ainvoke({"external_id": request.shipment_external_id})
            context.append({"source_id": f"shipment:{request.shipment_external_id}", "source_type": "shipment", "label": request.shipment_external_id, "content": shipment})
            payload = (shipment.get("shipment") or {}).get("payload") or {}
            location = location or payload.get("order_city") or payload.get("customer_city") or payload.get("order_country")
            yield {"type": "progress", "stage": "shipment", "label": "Shipment and prediction loaded" if shipment.get("found") else "Shipment not found", "status": "done", "duration": time.perf_counter()-started, "elapsed": time.perf_counter()-total_started}

        jobs = []
        if intent in {"weather", "combined"} and location:
            jobs.append(self._run_timed("weather", self.tools["weather_context"].ainvoke({"location": str(location)})))
            yield {"type": "progress", "stage": "weather", "label": f"Checking weather risk for {location}", "status": "running", "elapsed": time.perf_counter()-total_started}
        if intent in {"events", "combined"}:
            jobs.append(self._run_timed("events", self.tools["active_events"].ainvoke({"limit": 30})))
            yield {"type": "progress", "stage": "events", "label": "Checking active supply-chain disruptions", "status": "running", "elapsed": time.perf_counter()-total_started}
        if intent in {"knowledge", "combined"}:
            jobs.append(self._run_timed("knowledge", self.tools["search_enterprise_knowledge"].ainvoke({"query": request.query, "top_k": 4})))
            yield {"type": "progress", "stage": "knowledge", "label": "Searching company policies and documents", "status": "running", "elapsed": time.perf_counter()-total_started}

        if jobs:
            tasks = [asyncio.create_task(job) for job in jobs]
            for task in asyncio.as_completed(tasks):
                key, value, duration, error = await task
                if error:
                    yield {"type": "progress", "stage": key, "label": f"{key.title()} context unavailable", "status": "warning", "duration": duration, "elapsed": time.perf_counter()-total_started}
                    continue
                if key == "weather":
                    context.append({"source_id": f"weather:{location}", "source_type": "weather", "label": str(location), "content": value})
                    label = "Weather context loaded"
                elif key == "events":
                    context.append({"source_id": "events:active", "source_type": "events", "label": "Active supply-chain events", "content": value})
                    label = f"Checked {len(value)} active disruptions"
                else:
                    for item in value:
                        context.append({"source_id": f"doc:{item['id']}", "source_type": "document", "label": item.get("metadata", {}).get("filename", item["id"]), "content": item["text"], "score": item["score"]})
                    label = f"Retrieved {len(value)} relevant document sections"
                yield {"type": "progress", "stage": key, "label": label, "status": "done", "duration": duration, "elapsed": time.perf_counter()-total_started}

        # shipment-only intent already has its context; fallback knowledge when no context exists.
        if not context and intent == "shipment":
            yield {"type": "progress", "stage": "shipment", "label": "No shipment context available", "status": "warning", "elapsed": time.perf_counter()-total_started}

        generation_started = time.perf_counter()
        yield {"type": "progress", "stage": "answer", "label": "Generating grounded operational answer", "status": "running", "elapsed": time.perf_counter()-total_started}
        answer = await self.answer_llm.ainvoke(
            f"{SYSTEM}\nQuestion: {request.query}\nContext JSON: {json.dumps(context, default=str)}"
        )
        allowed = {item["source_id"] for item in context if item.get("source_id")}
        answer = answer.model_copy(update={"citations": [c for c in answer.citations if c.source_id in allowed]})
        if not context:
            answer = answer.model_copy(update={"confidence": "low", "citations": [], "limitations": [*answer.limitations, "No grounded SupplyMind context was available."]})
        yield {"type": "progress", "stage": "answer", "label": "Grounded answer ready", "status": "done", "duration": time.perf_counter()-generation_started, "elapsed": time.perf_counter()-total_started}
        yield {"type": "final", "answer": answer.model_dump(mode="json"), "total_duration": time.perf_counter()-total_started}
