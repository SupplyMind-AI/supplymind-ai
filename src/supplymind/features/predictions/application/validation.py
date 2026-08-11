"""Dataset-contract and data-quality validation."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from supplymind.features.predictions.domain.constants import (
    MODEL_FEATURES,
    SPLIT_TIMESTAMP_COLUMN,
    TARGET_COLUMN,
)


@dataclass(frozen=True)
class ValidationResult:
    """Result returned by a data validation check."""

    is_valid: bool
    errors: list[str]
    warnings: list[str]


# -------------------
# Required columns
# -------------------

def validate_required_columns(
    frame: pd.DataFrame,
    required_columns: list[str],
) -> ValidationResult:
    """Validate required-column presence."""

    missing = sorted(set(required_columns) - set(frame.columns))
    errors = [f"Missing required column: {column}" for column in missing]
    return ValidationResult(not errors, errors, [])


# -------------------
# Binary target
# -------------------

def validate_binary_target(frame: pd.DataFrame) -> ValidationResult:
    """Validate the V1 target domain and class presence."""

    if TARGET_COLUMN not in frame:
        return ValidationResult(
            False,
            [f"Missing target column: {TARGET_COLUMN}"],
            [],
        )

    target = frame[TARGET_COLUMN]
    errors: list[str] = []
    warnings: list[str] = []

    if target.isna().any():
        errors.append("Binary target contains missing values.")

    values = set(target.dropna().unique())
    if not values.issubset({0, 1, False, True}):
        errors.append(f"Binary target has unexpected values: {sorted(values)}")

    if target.nunique(dropna=True) < 2:
        errors.append("Binary target contains fewer than two classes.")

    rate = float(target.mean())
    if rate < 0.10 or rate > 0.90:
        warnings.append(f"Strong class imbalance detected: positive_rate={rate:.3f}")

    return ValidationResult(not errors, errors, warnings)


# -------------------
# Temporal column
# -------------------

def validate_split_timestamp(frame: pd.DataFrame) -> ValidationResult:
    """Validate the chronological split timestamp."""

    if SPLIT_TIMESTAMP_COLUMN not in frame:
        return ValidationResult(
            False,
            [f"Missing split timestamp: {SPLIT_TIMESTAMP_COLUMN}"],
            [],
        )

    parsed = pd.to_datetime(
        frame[SPLIT_TIMESTAMP_COLUMN],
        errors="coerce",
    )

    invalid = int(parsed.isna().sum())
    errors = []
    warnings = []

    if invalid == len(frame):
        errors.append("Split timestamp is completely invalid.")
    elif invalid:
        warnings.append(f"{invalid} rows have invalid split timestamps.")

    return ValidationResult(not errors, errors, warnings)


# -------------------
# Production feature contract
# -------------------

def validate_model_features(frame: pd.DataFrame) -> ValidationResult:
    """Validate that engineered model features are present."""

    return validate_required_columns(frame, MODEL_FEATURES)
