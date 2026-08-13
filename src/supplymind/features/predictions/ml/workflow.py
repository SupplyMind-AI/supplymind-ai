"""High-level reusable workflow used by notebooks, scripts, and retraining."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from supplymind.features.predictions.application.dataset import (
    canonicalize_syndelay,
    load_tabular_dataset,
)
from supplymind.features.predictions.application.validation import (
    validate_binary_target,
    validate_split_timestamp,
    validate_target_consistency,
)
from supplymind.features.predictions.domain.constants import (
    MODEL_INPUT_FEATURES,
    SPLIT_TIMESTAMP_COLUMN,
    TARGET_COLUMN,
)
from supplymind.features.predictions.ml.cleaning import clean_syndelay
from supplymind.features.predictions.ml.splitting import TemporalSplit, temporal_split


# -------------------
# Prepared model data
# -------------------

@dataclass(frozen=True)
class PreparedModelData:
    """Chronological raw model inputs and targets.

    Feature engineering is deliberately left inside the persisted sklearn
    pipeline so training, retraining, validation, test, and FastAPI inference
    all use the same learned transformations.
    """

    raw_split: TemporalSplit

    X_train: pd.DataFrame
    y_train: pd.Series

    X_validation: pd.DataFrame
    y_validation: pd.Series

    X_test: pd.DataFrame
    y_test: pd.Series


# -------------------
# Dataset preparation
# -------------------

def load_clean_syndelay(path: str | Path) -> pd.DataFrame:
    """Load, canonicalize, validate, and clean the SynDelay dataset."""

    raw = load_tabular_dataset(path)
    canonical = canonicalize_syndelay(raw)

    validations = [
        ("target consistency", validate_target_consistency(canonical)),
        ("binary target", validate_binary_target(canonical)),
        ("split timestamp", validate_split_timestamp(canonical)),
    ]

    for name, result in validations:
        if not result.is_valid:
            raise ValueError(
                f"SynDelay {name} validation failed: {result.errors}"
            )

    return clean_syndelay(canonical)


# -------------------
# Model data preparation
# -------------------

def prepare_model_data(frame: pd.DataFrame) -> PreparedModelData:
    """Create a leakage-safe chronological split for model training.

    This function performs only the temporal partition and raw feature/target
    selection. Learned feature engineering remains inside the model pipeline.
    """

    raw_split = temporal_split(frame, SPLIT_TIMESTAMP_COLUMN)

    def _features(partition: pd.DataFrame) -> pd.DataFrame:
        missing = [
            column for column in MODEL_INPUT_FEATURES
            if column not in partition.columns
        ]
        if missing:
            raise KeyError(f"Missing raw model input features: {missing}")
        return partition[MODEL_INPUT_FEATURES].copy()

    return PreparedModelData(
        raw_split=raw_split,
        X_train=_features(raw_split.train),
        y_train=raw_split.train[TARGET_COLUMN].copy(),
        X_validation=_features(raw_split.validation),
        y_validation=raw_split.validation[TARGET_COLUMN].copy(),
        X_test=_features(raw_split.test),
        y_test=raw_split.test[TARGET_COLUMN].copy(),
    )
