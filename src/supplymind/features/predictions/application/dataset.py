"""Dataset loading and SynDelay-to-SupplyMind canonicalization."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from supplymind.features.predictions.domain.constants import (
    DELAYED_CLASS,
    DELIVERY_OUTCOME_COLUMN,
    SOURCE_TARGET_COLUMN,
    SYNDELAY_COLUMNS,
    TARGET_COLUMN,
)


# -------------------
# Dataset loading
# -------------------

def load_tabular_dataset(path: str | Path) -> pd.DataFrame:
    """Load a local CSV or Parquet file without mutating its contents."""

    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    suffix = dataset_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(dataset_path, low_memory=False)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(dataset_path)

    raise ValueError(
        f"Unsupported dataset format '{suffix}'. Expected CSV or Parquet."
    )


# -------------------
# Column normalization
# -------------------

def normalize_column_names(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with deterministic snake_case column names."""

    normalized = frame.copy()
    normalized.columns = (
        normalized.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return normalized


# -------------------
# Excel date conversion
# -------------------

def excel_serial_to_datetime(series: pd.Series) -> pd.Series:
    """Convert Excel serial dates to pandas timestamps.

    SynDelay stores `order_date` and `shipping_date` as Excel serial-day
    numbers. Fractional values represent the time of day.
    """

    numeric = pd.to_numeric(series, errors="coerce")
    return pd.to_datetime(
        numeric,
        unit="D",
        origin="1899-12-30",
        errors="coerce",
    )


# -------------------
# Binary target mapping
# -------------------

def add_binary_delay_target(frame: pd.DataFrame) -> pd.DataFrame:
    """Preserve the source label and create SupplyMind's V1 binary target.

    SynDelay:
        0 = early
        1 = on-time
        2 = delayed

    SupplyMind V1:
        0 = not delayed (source classes 0 and 1)
        1 = delayed (source class 2)
    """

    if SOURCE_TARGET_COLUMN not in frame.columns:
        raise KeyError(f"Missing source target '{SOURCE_TARGET_COLUMN}'.")

    result = frame.copy()
    source = pd.to_numeric(result[SOURCE_TARGET_COLUMN], errors="raise")

    unexpected = sorted(set(source.unique()) - {0, 1, 2})
    if unexpected:
        raise ValueError(f"Unexpected SynDelay labels: {unexpected}")

    result[DELIVERY_OUTCOME_COLUMN] = source.astype("int8")
    result[TARGET_COLUMN] = (source == DELAYED_CLASS).astype("int8")
    return result


# -------------------
# SynDelay canonicalization
# -------------------

def canonicalize_syndelay(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize SynDelay into the stable SupplyMind training contract."""

    canonical = normalize_column_names(frame)

    missing = sorted(set(SYNDELAY_COLUMNS) - set(canonical.columns))
    if missing:
        raise ValueError(
            "SynDelay schema does not match the expected V1 contract. "
            f"Missing columns: {missing}"
        )

    canonical = canonical[SYNDELAY_COLUMNS].copy()
    canonical["order_date"] = excel_serial_to_datetime(canonical["order_date"])
    canonical["shipping_date"] = excel_serial_to_datetime(
        canonical["shipping_date"]
    )
    canonical = add_binary_delay_target(canonical)
    return canonical
