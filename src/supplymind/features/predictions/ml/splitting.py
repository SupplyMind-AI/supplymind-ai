"""Leakage-safe chronological train/validation/test splitting."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from supplymind.features.predictions.domain.constants import (
    TEST_FRACTION,
    TRAIN_FRACTION,
    VALIDATION_FRACTION,
)


@dataclass(frozen=True)
class TemporalSplit:
    """Chronologically ordered data partitions."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


# -------------------
# Temporal split
# -------------------

def temporal_split(
    frame: pd.DataFrame,
    timestamp_column: str,
    *,
    train_fraction: float = TRAIN_FRACTION,
    validation_fraction: float = VALIDATION_FRACTION,
) -> TemporalSplit:
    """Split observations in chronological order without shuffling."""

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1.")
    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be between 0 and 1.")
    if train_fraction + validation_fraction >= 1:
        raise ValueError("Fractions must leave a non-empty test set.")

    ordered = frame.copy()
    ordered[timestamp_column] = pd.to_datetime(
        ordered[timestamp_column],
        errors="raise",
    )
    ordered = ordered.sort_values(
        [timestamp_column],
        kind="mergesort",
    ).reset_index(drop=True)

    train_end = int(len(ordered) * train_fraction)
    validation_end = int(
        len(ordered) * (train_fraction + validation_fraction)
    )

    split = TemporalSplit(
        train=ordered.iloc[:train_end].copy(),
        validation=ordered.iloc[train_end:validation_end].copy(),
        test=ordered.iloc[validation_end:].copy(),
    )

    _assert_temporal_order(split, timestamp_column)
    return split


# -------------------
# Split validation
# -------------------

def _assert_temporal_order(
    split: TemporalSplit,
    timestamp_column: str,
) -> None:
    """Fail if future observations leak into earlier partitions."""

    if split.train.empty or split.validation.empty or split.test.empty:
        raise ValueError("Temporal split produced an empty partition.")

    if (
        split.train[timestamp_column].max()
        > split.validation[timestamp_column].min()
    ):
        raise ValueError("Train and validation periods overlap.")

    if (
        split.validation[timestamp_column].max()
        > split.test[timestamp_column].min()
    ):
        raise ValueError("Validation and test periods overlap.")
