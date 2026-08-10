"""Validation helpers for training and inference datasets."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


# -------------------
# Validation result
# Structured result returned by dataset validation.
# -------------------

@dataclass(frozen=True)
class ValidationResult:

    is_valid: bool
    errors: list[str]
    warnings: list[str]


# -------------------
# Schema validation
# Validate that all required columns are present.
# -------------------

def validate_required_columns(
    frame: pd.DataFrame,
    required_columns: list[str],
) -> ValidationResult:
    """"""

    missing = sorted(set(required_columns) - set(frame.columns))
    errors = [f"Missing required column: {column}" for column in missing]

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=[],
    )


# -------------------
# Target validation
# -------------------

def validate_binary_target(
    frame: pd.DataFrame,
    target_column: str,
) -> ValidationResult:
    """Validate that a target contains only binary values and no nulls."""

    errors: list[str] = []
    warnings: list[str] = []

    if target_column not in frame.columns:
        return ValidationResult(
            is_valid=False,
            errors=[f"Target column not found: {target_column}"],
            warnings=[],
        )

    if frame[target_column].isna().any():
        errors.append(f"Target '{target_column}' contains missing values.")

    values = set(frame[target_column].dropna().unique().tolist())
    if not values.issubset({0, 1, False, True}):
        errors.append(
            f"Target '{target_column}' must be binary; found values: {sorted(values)}"
        )

    positive_rate = float(frame[target_column].mean())
    if positive_rate < 0.05 or positive_rate > 0.95:
        warnings.append(
            f"Target is strongly imbalanced; positive rate={positive_rate:.3f}."
        )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
    )


# -------------------
# Temporal validation
# -------------------

def validate_timestamp_column(
    frame: pd.DataFrame,
    timestamp_column: str,
) -> ValidationResult:
    """Validate that a timestamp column can be parsed and is not fully missing."""

    if timestamp_column not in frame.columns:
        return ValidationResult(
            is_valid=False,
            errors=[f"Timestamp column not found: {timestamp_column}"],
            warnings=[],
        )

    parsed = pd.to_datetime(frame[timestamp_column], errors="coerce")
    invalid_count = int(parsed.isna().sum())

    errors: list[str] = []
    warnings: list[str] = []

    if invalid_count == len(frame):
        errors.append(f"Timestamp '{timestamp_column}' could not be parsed.")
    elif invalid_count > 0:
        warnings.append(
            f"Timestamp '{timestamp_column}' has {invalid_count} unparseable values."
        )

    return ValidationResult(
        is_valid=not errors,
        errors=errors,
        warnings=warnings,
    )
