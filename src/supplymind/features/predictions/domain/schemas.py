"""Typed prediction-domain schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# -------------------
# Prediction input
# -------------------

class ShipmentFeatures(BaseModel):
    """Raw business features accepted by the prediction service.

    Engineered fields such as order month and city frequency are intentionally
    absent: they are produced inside the persisted model pipeline.
    """

    model_config = ConfigDict(extra="forbid")

    shipment_id: str | None = None
    prediction_at: datetime | None = None

    # -------------------
    # Raw numerical features
    # -------------------

    profit_per_order: float | None = None
    sales_per_customer: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    order_item_discount: float | None = None
    order_item_discount_rate: float | None = None
    order_item_product_price: float | None = None
    order_item_profit_ratio: float | None = None
    order_item_quantity: float | None = None
    sales: float | None = None
    order_item_total_amount: float | None = None
    order_profit_per_order: float | None = None
    product_price: float | None = None

    # -------------------
    # Raw temporal/geography features
    # -------------------

    order_date: datetime
    customer_city: str | None = None
    order_city: str | None = None
    order_state: str | None = None

    # -------------------
    # Raw categorical features
    # -------------------

    payment_type: str | None = None
    category_name: str | None = None
    customer_country: str | None = None
    customer_segment: str | None = None
    customer_state: str | None = None
    department_name: str | None = None
    market: str | None = None
    order_country: str | None = None
    order_region: str | None = None
    product_name: str | None = None
    shipping_mode: str | None = None


# -------------------
# Prediction output
# -------------------

class DelayPrediction(BaseModel):
    """Binary delay prediction returned by the champion pipeline."""

    shipment_id: str | None = None
    delayed: bool
    delay_probability: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    risk_level: str
    model_name: str
    model_version: str


# -------------------
# Model metrics
# -------------------

class ModelMetrics(BaseModel):
    """Evaluation metrics stored for a model version."""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    average_precision: float | None = None


# -------------------
# Model metadata
# -------------------

class ModelMetadata(BaseModel):
    """Metadata persisted with a trained candidate or champion model."""

    model_name: str
    model_version: str
    trained_at: datetime
    source_dataset: str
    target_column: str
    split_timestamp_column: str
    feature_columns: list[str]
    threshold: float = Field(ge=0.0, le=1.0)
    validation_metrics: ModelMetrics
    test_metrics: ModelMetrics | None = None
