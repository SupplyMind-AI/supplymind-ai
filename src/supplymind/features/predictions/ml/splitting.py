"""Chronological train, validation, and test splitting."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


# -------------------
# Split result
# -------------------

@dataclass(frozen=True)
class TemporalSplit:
    """Container for chronological dataset partitions."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


# -------------------
# Temporal split
# -------------------

def temporal_train_validation_test_split(
    frame: pd.DataFrame,
    timestamp_column: str,
    *,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> TemporalSplit:
    """Split a dataset chronologically without shuffling."""

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")
    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1.")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("Train and validation fractions must leave a test set.")
    if timestamp_column not in frame.columns:
        raise KeyError(f"Timestamp column not found: {timestamp_column}")

    ordered = frame.copy()
    ordered[timestamp_column] = pd.to_datetime(
        ordered[timestamp_column],
        errors="raise",
    )
    ordered = ordered.sort_values(timestamp_column).reset_index(drop=True)

    train_end = int(len(ordered) * train_fraction)
    validation_end = int(
        len(ordered) * (train_fraction + validation_fraction)
    )

    train = ordered.iloc[:train_end].copy()
    validation = ordered.iloc[train_end:validation_end].copy()
    test = ordered.iloc[validation_end:].copy()

    if train[timestamp_column].max() > validation[timestamp_column].min():
        raise ValueError("Training and validation periods overlap.")
    if validation[timestamp_column].max() > test[timestamp_column].min():
        raise ValueError("Validation and test periods overlap.")

    return TemporalSplit(
        train=train,
        validation=validation,
        test=test,
    )
