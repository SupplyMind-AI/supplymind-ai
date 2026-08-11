"""Production feature engineering for shipment-delay prediction."""

from __future__ import annotations

import pandas as pd

from supplymind.features.predictions.domain.constants import (
    CATEGORICAL_FEATURES,
    IDENTIFIER_COLUMNS,
    MODEL_FEATURES,
    NUMERICAL_FEATURES,
    POST_PREDICTION_OR_AMBIGUOUS_COLUMNS,
    REDUNDANT_CATEGORY_ID_COLUMNS,
)


# -------------------
# Order-date features
# -------------------

def add_order_date_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create calendar features known at order/planning time."""

    result = frame.copy()
    order_date = pd.to_datetime(result["order_date"], errors="coerce")

    result["order_year"] = order_date.dt.year.astype("Int16")
    result["order_month"] = order_date.dt.month.astype("Int8")
    result["order_quarter"] = order_date.dt.quarter.astype("Int8")
    result["order_week"] = order_date.dt.isocalendar().week.astype("Int16")
    result["order_day"] = order_date.dt.day.astype("Int8")
    result["order_weekday"] = order_date.dt.weekday.astype("Int8")
    result["order_hour"] = order_date.dt.hour.astype("Int8")
    result["order_is_weekend"] = (
        order_date.dt.weekday.ge(5).astype("int8")
    )

    return result


# -------------------
# Frequency encoding
# -------------------

def add_frequency_features(
    frame: pd.DataFrame,
    *,
    reference: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Frequency-encode selected high-cardinality geography fields.

    Frequency encoding avoids thousands of one-hot columns and does not use
    the target, so it is safer than target encoding.

    During validation/test/inference, pass the training frame as `reference`
    so frequencies are learned only from training data.
    """

    result = frame.copy()
    reference_frame = frame if reference is None else reference

    for column in ["customer_city", "order_city", "order_state"]:
        frequencies = reference_frame[column].value_counts(normalize=True)
        result[f"{column}_frequency"] = (
            result[column].map(frequencies).fillna(0.0).astype("float32")
        )

    return result


# -------------------
# Leakage removal
# -------------------

def columns_excluded_from_model() -> list[str]:
    """Return columns deliberately excluded from model inputs."""

    return sorted(
        set(
            IDENTIFIER_COLUMNS
            + REDUNDANT_CATEGORY_ID_COLUMNS
            + POST_PREDICTION_OR_AMBIGUOUS_COLUMNS
            + [
                "label",
                "delivery_outcome",
                "is_delayed",
                "customer_zipcode",
                "customer_city",
                "order_city",
                "order_state",
                "order_date",
            ]
        )
    )


# -------------------
# Feature engineering
# -------------------

def engineer_features(
    frame: pd.DataFrame,
    *,
    frequency_reference: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Create all V1 deterministic model features."""

    featured = add_order_date_features(frame)
    featured = add_frequency_features(
        featured,
        reference=frequency_reference,
    )
    return featured


# -------------------
# Feature matrix
# -------------------

def build_feature_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Return model inputs in an explicit, deterministic column order."""

    missing = [column for column in MODEL_FEATURES if column not in frame]
    if missing:
        raise KeyError(f"Missing engineered model features: {missing}")

    return frame[MODEL_FEATURES].copy()


def feature_groups() -> tuple[list[str], list[str]]:
    """Return the stable numerical and categorical feature groups."""

    return list(NUMERICAL_FEATURES), list(CATEGORICAL_FEATURES)
