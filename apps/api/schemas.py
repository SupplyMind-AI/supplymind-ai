from __future__ import annotations
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

# -------------------
# Prediction
# -------------------

class PredictionRequest(BaseModel):
    external_id: str = Field(
        min_length=1,
        max_length=128,
    )
    order_date: datetime
    features: dict[str, Any]


# -------------------
# Semantic search
# -------------------

class SemanticSearchRequest(BaseModel):
    query: str = Field(
        min_length=2,
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


# -------------------
# Enterprise document ingestion
# -------------------

class DocumentIngestionRequest(BaseModel):
    filename: str = Field(
        min_length=1,
    )
    source_name: str = "enterprise"
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


# -------------------
# Retraining
# -------------------

class RetrainingRequest(BaseModel):
    reason: str = Field(
        min_length=3,
    )
    base_model_version_id: str | None = None
