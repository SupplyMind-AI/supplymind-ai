"""Dataset-contract and data-quality validation."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from supplymind.features.predictions.domain.constants import (
    DELAYED_CLASS,
    DELIVERY_OUTCOME_COLUMN,
    MODEL_FEATURES,
    SOURCE_TARGET_COLUMN,
    SPLIT_TIMESTAMP_COLUMN,
    TARGET_COLUMN,
)


# -------------------
# Validation result
# -------------------

@dataclass(frozen=True)
class ValidationResult:
    """Result returned by a dataset validation check."""

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
    """Validate that all required columns are present."""

    missing = sorted(set(required_columns) - set(frame.columns))
    errors = [f"Missing required column: {column}" for column in missing]

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=[],
    )


# -------------------
# Target consistency
# -------------------

def validate_target_consistency(frame: pd.DataFrame) -> ValidationResult:
    """Validate SupplyMind's canonical targets against the SynDelay label."""

    required_columns = [
        SOURCE_TARGET_COLUMN,
        DELIVERY_OUTCOME_COLUMN,
        TARGET_COLUMN,
    ]
    required_result = validate_required_columns(frame, required_columns)
    if not required_result.is_valid:
        return required_result

    errors: list[str] = []

    if not (
        frame[SOURCE_TARGET_COLUMN]
        == frame[DELIVERY_OUTCOME_COLUMN]
    ).all():
        errors.append(
            f"`{SOURCE_TARGET_COLUMN}` and "
            f"`{DELIVERY_OUTCOME_COLUMN}` are inconsistent."
        )

    expected_binary = (
        frame[SOURCE_TARGET_COLUMN] == DELAYED_CLASS
    ).astype("int8")

    if not (frame[TARGET_COLUMN] == expected_binary).all():
        errors.append(
            f"`{TARGET_COLUMN}` is inconsistent with "
            f"delayed class {DELAYED_CLASS}."
        )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=[],
    )


# -------------------
# Binary target
# -------------------

def validate_binary_target(frame: pd.DataFrame) -> ValidationResult:
    """Validate the production binary target domain and class balance."""

    if TARGET_COLUMN not in frame.columns:
        return ValidationResult(
            is_valid=False,
            errors=[f"Missing binary target: {TARGET_COLUMN}"],
            warnings=[],
        )

    target = frame[TARGET_COLUMN]
    errors: list[str] = []
    warnings: list[str] = []

    if target.isna().any():
        errors.append(f"`{TARGET_COLUMN}` contains missing values.")

    values = set(target.dropna().unique().tolist())
    if not values.issubset({0, 1}):
        errors.append(
            f"`{TARGET_COLUMN}` must contain only 0 and 1. "
            f"Found: {sorted(values)}"
        )

    if target.nunique(dropna=True) < 2:
        errors.append(f"`{TARGET_COLUMN}` contains fewer than two classes.")

    if not target.empty:
        delayed_rate = float(target.mean())
        if delayed_rate < 0.10 or delayed_rate > 0.90:
            warnings.append(
                "Strong class imbalance detected: "
                f"delayed_rate={delayed_rate:.3f}"
            )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
    )


# -------------------
# Temporal column
# -------------------

def validate_split_timestamp(frame: pd.DataFrame) -> ValidationResult:
    """Validate the timestamp used for chronological splitting."""

    if SPLIT_TIMESTAMP_COLUMN not in frame.columns:
        return ValidationResult(
            is_valid=False,
            errors=[f"Missing split timestamp: {SPLIT_TIMESTAMP_COLUMN}"],
            warnings=[],
        )

    parsed = pd.to_datetime(
        frame[SPLIT_TIMESTAMP_COLUMN],
        errors="coerce",
    )
    invalid_count = int(parsed.isna().sum())

    errors: list[str] = []
    warnings: list[str] = []

    if invalid_count == len(frame):
        errors.append(f"`{SPLIT_TIMESTAMP_COLUMN}` is completely invalid.")
    elif invalid_count > 0:
        warnings.append(
            f"`{SPLIT_TIMESTAMP_COLUMN}` contains "
            f"{invalid_count} invalid timestamps."
        )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
    )


# -------------------
# Production feature contract
# -------------------

def validate_model_features(frame: pd.DataFrame) -> ValidationResult:
    """Validate that all engineered production features are present."""

    return validate_required_columns(frame, MODEL_FEATURES)
