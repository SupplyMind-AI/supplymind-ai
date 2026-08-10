"""Dataset loading and source-to-canonical mapping helpers."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


# -------------------
# Dataset loading
# -------------------

def load_tabular_dataset(path: str | Path) -> pd.DataFrame:

    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    suffix = dataset_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(dataset_path, low_memory=False)
    if suffix in {".parquet", ".pq"}:
        return pd.read_parquet(dataset_path)

    raise ValueError(
        f"Unsupported dataset format '{suffix}'. Use CSV or Parquet."
    )


# -------------------
# Column normalization
# Return a copy with normalized snake_case column names.
# -------------------

def normalize_column_names(frame: pd.DataFrame) -> pd.DataFrame:

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
# Source adapter placeholder
# Map SynDelay columns into the SupplyMind canonical schema.
# -------------------

def map_syndelay_to_canonical(frame: pd.DataFrame) -> pd.DataFrame:

    normalized = normalize_column_names(frame)

    column_mapping: dict[str, str] = {
        # Example only — replace after inspecting the downloaded dataset:
        # "shipment_identifier": "shipment_id",
        # "planned_delivery_timestamp": "planned_delivery_at",
        # "delivery_status": "is_delayed",
    }

    canonical = normalized.rename(columns=column_mapping)
    return canonical
