"""High-level reusable workflow used by notebooks, scripts and retraining."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from supplymind.features.predictions.application.dataset import (
    canonicalize_syndelay,
    load_tabular_dataset,
)
from supplymind.features.predictions.domain.constants import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    SPLIT_TIMESTAMP_COLUMN,
    TARGET_COLUMN,
)
from supplymind.features.predictions.ml.cleaning import clean_syndelay
from supplymind.features.predictions.ml.features import (
    build_feature_matrix,
    engineer_features,
)
from supplymind.features.predictions.ml.splitting import TemporalSplit, temporal_split


@dataclass(frozen=True)
class PreparedModelData:
    """Prepared chronological datasets and model matrices."""

    raw_split: TemporalSplit
    X_train: pd.DataFrame
    y_train: pd.Series
    X_validation: pd.DataFrame
    y_validation: pd.Series
    X_test: pd.DataFrame
    y_test: pd.Series


# -------------------
# Canonical dataset
# -------------------

def load_clean_syndelay(path) -> pd.DataFrame:
    """Load, canonicalize and clean the source dataset."""

    raw = load_tabular_dataset(path)
    canonical = canonicalize_syndelay(raw)
    return clean_syndelay(canonical)


# -------------------
# Model data preparation
# -------------------

def prepare_model_data(frame: pd.DataFrame) -> PreparedModelData:
    """Create a leakage-safe temporal split and engineered matrices.

    Frequency encodings for validation and test are learned from the training
    partition only.
    """

    raw_split = temporal_split(frame, SPLIT_TIMESTAMP_COLUMN)

    train_featured = engineer_features(raw_split.train)
    validation_featured = engineer_features(
        raw_split.validation,
        frequency_reference=raw_split.train,
    )
    test_featured = engineer_features(
        raw_split.test,
        frequency_reference=raw_split.train,
    )

    return PreparedModelData(
        raw_split=raw_split,
        X_train=build_feature_matrix(train_featured),
        y_train=train_featured[TARGET_COLUMN].copy(),
        X_validation=build_feature_matrix(validation_featured),
        y_validation=validation_featured[TARGET_COLUMN].copy(),
        X_test=build_feature_matrix(test_featured),
        y_test=test_featured[TARGET_COLUMN].copy(),
    )
