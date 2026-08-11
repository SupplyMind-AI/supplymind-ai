"""Constants and explicit feature contracts for delay prediction."""

from __future__ import annotations

# -------------------
# Dataset contract
# -------------------

SOURCE_TARGET_COLUMN = "label"
DELIVERY_OUTCOME_COLUMN = "delivery_outcome"
TARGET_COLUMN = "is_delayed"
SPLIT_TIMESTAMP_COLUMN = "order_date"

EARLY_CLASS = 0
ON_TIME_CLASS = 1
DELAYED_CLASS = 2

# -------------------
# Temporal split
# -------------------

TRAIN_FRACTION = 0.70
VALIDATION_FRACTION = 0.15
TEST_FRACTION = 0.15
RANDOM_STATE = 42

# -------------------
# Decision threshold
# -------------------

DEFAULT_DECISION_THRESHOLD = 0.50

# -------------------
# Source schema
# -------------------

SYNDELAY_COLUMNS = [
    "payment_type",
    "profit_per_order",
    "sales_per_customer",
    "category_id",
    "category_name",
    "customer_city",
    "customer_country",
    "customer_id",
    "customer_segment",
    "customer_state",
    "customer_zipcode",
    "department_id",
    "department_name",
    "latitude",
    "longitude",
    "market",
    "order_city",
    "order_country",
    "order_customer_id",
    "order_date",
    "order_id",
    "order_item_cardprod_id",
    "order_item_discount",
    "order_item_discount_rate",
    "order_item_id",
    "order_item_product_price",
    "order_item_profit_ratio",
    "order_item_quantity",
    "sales",
    "order_item_total_amount",
    "order_profit_per_order",
    "order_region",
    "order_state",
    "order_status",
    "product_card_id",
    "product_category_id",
    "product_name",
    "product_price",
    "shipping_date",
    "shipping_mode",
    "label",
]

# -------------------
# Leakage / unsafe columns
# -------------------

# shipping_date is excluded because SupplyMind scores at order/planning time.
# order_status is excluded because the source field may represent a later
# lifecycle state rather than the state known at prediction time.
POST_PREDICTION_OR_AMBIGUOUS_COLUMNS = [
    "shipping_date",
    "order_status",
]

# High-cardinality identifiers are not business features.
IDENTIFIER_COLUMNS = [
    "customer_id",
    "order_customer_id",
    "order_id",
    "order_item_id",
    "order_item_cardprod_id",
    "product_card_id",
]

# Redundant ID representations where a semantic category/name is retained.
REDUNDANT_CATEGORY_ID_COLUMNS = [
    "category_id",
    "department_id",
    "product_category_id",
]

# -------------------
# Base production features
# -------------------

NUMERICAL_FEATURES = [
    "profit_per_order",
    "sales_per_customer",
    "latitude",
    "longitude",
    "order_item_discount",
    "order_item_discount_rate",
    "order_item_product_price",
    "order_item_profit_ratio",
    "order_item_quantity",
    "sales",
    "order_item_total_amount",
    "order_profit_per_order",
    "product_price",
    "order_year",
    "order_month",
    "order_quarter",
    "order_week",
    "order_day",
    "order_weekday",
    "order_hour",
    "order_is_weekend",
    "customer_city_frequency",
    "order_city_frequency",
    "order_state_frequency",
]

CATEGORICAL_FEATURES = [
    "payment_type",
    "category_name",
    "customer_country",
    "customer_segment",
    "customer_state",
    "department_name",
    "market",
    "order_country",
    "order_region",
    "product_name",
    "shipping_mode",
]

MODEL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
