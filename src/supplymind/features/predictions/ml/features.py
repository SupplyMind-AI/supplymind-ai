"""Feature engineering for shipment-delay prediction."""

from __future__ import annotations

import pandas as pd


# -------------------
# Datetime features
# -------------------

def add_datetime_features(
    frame: pd.DataFrame,
    timestamp_columns: list[str],
) -> pd.DataFrame:
    """Extract stable calendar features from configured timestamps."""

    featured = frame.copy()

    for column in timestamp_columns:
        if column not in featured.columns:
            continue

        values = pd.to_datetime(featured[column], errors="coerce")
        featured[f"{column}_year"] = values.dt.year
        featured[f"{column}_month"] = values.dt.month
        featured[f"{column}_weekday"] = values.dt.weekday
        featured[f"{column}_hour"] = values.dt.hour

    return featured


# -------------------
# Lead-time features
# -------------------

def add_planned_lead_time(
    frame: pd.DataFrame,
    departure_column: str,
    delivery_column: str,
    output_column: str = "planned_lead_time_days",
) -> pd.DataFrame:
    """Calculate planned lead time using information available before delivery."""

    featured = frame.copy()

    if departure_column not in featured.columns:
        return featured
    if delivery_column not in featured.columns:
        return featured

    departure = pd.to_datetime(featured[departure_column], errors="coerce")
    delivery = pd.to_datetime(featured[delivery_column], errors="coerce")

    featured[output_column] = (
        delivery - departure
    ).dt.total_seconds() / 86_400

    return featured
