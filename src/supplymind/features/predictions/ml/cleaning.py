"""Deterministic cleaning rules shared by training and inference."""

from __future__ import annotations

import pandas as pd


# -------------------
# String normalization
# -------------------

def normalize_strings(frame: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace from categorical values without changing semantics."""

    result = frame.copy()
    columns = result.select_dtypes(include=["object", "string"]).columns

    for column in columns:
        result[column] = result[column].astype("string").str.strip()

    return result


# -------------------
# Duplicate handling
# -------------------

def remove_exact_duplicates(frame: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows and reset the index."""

    return frame.drop_duplicates().reset_index(drop=True)


# -------------------
# Cleaning pipeline
# -------------------

def clean_syndelay(frame: pd.DataFrame) -> pd.DataFrame:
    """Apply only deterministic and production-safe cleaning."""

    cleaned = normalize_strings(frame)
    cleaned = remove_exact_duplicates(cleaned)
    return cleaned
