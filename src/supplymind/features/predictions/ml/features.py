"""Production feature engineering for shipment-delay prediction."""

from __future__ import annotations

from collections.abc import Mapping

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

from supplymind.features.predictions.domain.constants import (
    CATEGORICAL_FEATURES,
    FREQUENCY_SOURCE_FEATURES,
    IDENTIFIER_COLUMNS,
    MODEL_FEATURES,
    NUMERICAL_FEATURES,
    POST_PREDICTION_OR_AMBIGUOUS_COLUMNS,
    REDUNDANT_CATEGORY_ID_COLUMNS,
    TARGET_COLUMNS,
)


# -------------------
# Order-date features
# -------------------

def add_order_date_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic calendar features known at prediction time."""

    result = frame.copy()
    order_date = pd.to_datetime(result["order_date"], errors="coerce")

    result["order_year"] = order_date.dt.year.astype("Int16")
    result["order_month"] = order_date.dt.month.astype("Int8")
    result["order_quarter"] = order_date.dt.quarter.astype("Int8")
    result["order_week"] = order_date.dt.isocalendar().week.astype("Int16")
    result["order_day"] = order_date.dt.day.astype("Int8")
    result["order_weekday"] = order_date.dt.weekday.astype("Int8")
    result["order_hour"] = order_date.dt.hour.astype("Int8")
    result["order_is_weekend"] = order_date.dt.weekday.ge(5).astype("int8")

    return result


# -------------------
# Frequency maps
# -------------------

def learn_frequency_maps(
    frame: pd.DataFrame,
) -> dict[str, dict[object, float]]:
    """Learn frequency maps for high-cardinality categorical fields."""

    maps: dict[str, dict[object, float]] = {}

    for column in FREQUENCY_SOURCE_FEATURES:
        if column not in frame.columns:
            raise KeyError(f"Missing frequency source feature: {column}")

        frequencies = frame[column].value_counts(
            normalize=True,
            dropna=False,
        )
        maps[column] = frequencies.to_dict()

    return maps


def apply_frequency_maps(
    frame: pd.DataFrame,
    frequency_maps: Mapping[str, Mapping[object, float]],
) -> pd.DataFrame:
    """Apply training-time frequency maps to any dataset or inference batch."""

    result = frame.copy()

    for column in FREQUENCY_SOURCE_FEATURES:
        if column not in result.columns:
            raise KeyError(f"Missing frequency source feature: {column}")

        mapping = frequency_maps[column]
        result[f"{column}_frequency"] = (
            result[column]
            .map(mapping)
            .fillna(0.0)
            .astype("float32")
        )

    return result


# -------------------
# Persistable feature transformer
# -------------------

class ShipmentFeatureEngineer(BaseEstimator, TransformerMixin):
    """Sklearn transformer that learns and applies V1 feature engineering.

    The transformer is persisted inside the model pipeline, which guarantees
    that FastAPI inference and retraining reuse the same frequency maps learned
    from the training partition.
    """

    def fit(self, X: pd.DataFrame, y=None):
        """Learn training-only state required by feature engineering."""

        frame = self._validate_frame(X)
        self.frequency_maps_ = learn_frequency_maps(frame)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Create deterministic and learned features for a new batch."""

        if not hasattr(self, "frequency_maps_"):
            raise RuntimeError("ShipmentFeatureEngineer must be fitted first.")

        frame = self._validate_frame(X)
        featured = add_order_date_features(frame)
        featured = apply_frequency_maps(featured, self.frequency_maps_)
        return featured

    @staticmethod
    def _validate_frame(X) -> pd.DataFrame:
        if not isinstance(X, pd.DataFrame):
            raise TypeError(
                "ShipmentFeatureEngineer expects a pandas DataFrame input."
            )
        return X.copy()


# -------------------
# Analysis convenience helper
# -------------------

def engineer_features(
    frame: pd.DataFrame,
    *,
    frequency_reference: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Engineer features for EDA/notebook inspection.

    Production model training uses `ShipmentFeatureEngineer` inside the sklearn
    pipeline. This helper exists for transparent notebook analysis only.
    """

    reference = frame if frequency_reference is None else frequency_reference
    transformer = ShipmentFeatureEngineer().fit(reference)
    return transformer.transform(frame)


# -------------------
# Leakage documentation
# -------------------

def columns_excluded_from_model() -> list[str]:
    """Return columns deliberately excluded from model inputs."""

    return sorted(
        set(
            IDENTIFIER_COLUMNS
            + REDUNDANT_CATEGORY_ID_COLUMNS
            + POST_PREDICTION_OR_AMBIGUOUS_COLUMNS
            + TARGET_COLUMNS
            + [
                "customer_zipcode",
            ]
        )
    )


# -------------------
# Feature matrix
# -------------------

def build_feature_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Return engineered model features in deterministic column order."""

    missing = [column for column in MODEL_FEATURES if column not in frame]
    if missing:
        raise KeyError(f"Missing engineered model features: {missing}")

    return frame[MODEL_FEATURES].copy()


def feature_groups() -> tuple[list[str], list[str]]:
    """Return the stable numerical and categorical feature groups."""

    return list(NUMERICAL_FEATURES), list(CATEGORICAL_FEATURES)
