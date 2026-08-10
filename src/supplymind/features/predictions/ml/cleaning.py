"""Deterministic cleaning operations for shipment data."""

from __future__ import annotations

import pandas as pd


# -------------------
# Data cleaning
# -------------------

def clean_shipment_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply deterministic, non-learned cleaning rules.

    This function must remain safe for training, validation, test,
    monitoring, retraining, and inference datasets.
    """

    cleaned = frame.copy()

    # -------------------
    # Remove exact duplicates
    # -------------------

    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    # -------------------
    # Normalize string values
    # -------------------

    string_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for column in string_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    return cleaned
