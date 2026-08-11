"""Generate repeatable EDA artifacts for SynDelay."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from supplymind.features.predictions.domain.constants import TARGET_COLUMN
from supplymind.features.predictions.ml.feature_selection import (
    chi_square_categorical_report,
    mutual_information_report,
    numeric_correlation_report,
)
from supplymind.features.predictions.ml.features import engineer_features, feature_groups
from supplymind.features.predictions.ml.workflow import load_clean_syndelay
from supplymind.features.predictions.ml.splitting import temporal_split
from supplymind.features.predictions.domain.constants import SPLIT_TIMESTAMP_COLUMN


DATASET_PATH = Path("data/raw/syndelay/syndelay_v1.csv")
REPORT_DIR = Path("reports/eda")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    frame = load_clean_syndelay(DATASET_PATH)
    # Statistical feature diagnostics use the training period only.
    split = temporal_split(frame, SPLIT_TIMESTAMP_COLUMN)
    featured = engineer_features(split.train)
    numerical, categorical = feature_groups()

    # -------------------
    # Dataset profile
    # -------------------

    profile = pd.DataFrame(
        {
            "column": frame.columns,
            "dtype": frame.dtypes.astype(str).values,
            "missing_count": frame.isna().sum().values,
            "missing_rate": frame.isna().mean().values,
            "unique_count": frame.nunique(dropna=True).values,
        }
    )
    profile.to_csv(REPORT_DIR / "dataset_profile.csv", index=False)

    # -------------------
    # Target distribution
    # -------------------

    target_distribution = (
        frame[TARGET_COLUMN]
        .value_counts()
        .sort_index()
        .rename_axis("is_delayed")
        .reset_index(name="count")
    )
    target_distribution["rate"] = (
        target_distribution["count"] / len(frame)
    )
    target_distribution.to_csv(
        REPORT_DIR / "target_distribution.csv",
        index=False,
    )

    target_distribution.plot(
        kind="bar",
        x="is_delayed",
        y="count",
        legend=False,
        title="SupplyMind V1 Binary Target",
    )
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "target_distribution.png", dpi=150)
    plt.close()

    # -------------------
    # Shipping-mode relationship
    # -------------------

    shipping_mode = pd.crosstab(
        frame["shipping_mode"],
        frame[TARGET_COLUMN],
        normalize="index",
    )
    shipping_mode.to_csv(REPORT_DIR / "shipping_mode_vs_target.csv")

    shipping_mode.plot(
        kind="bar",
        stacked=True,
        figsize=(9, 5),
        title="Delay Outcome by Shipping Mode",
    )
    plt.ylabel("Proportion")
    plt.tight_layout()
    plt.savefig(REPORT_DIR / "shipping_mode_vs_target.png", dpi=150)
    plt.close()

    # -------------------
    # Statistical reports
    # -------------------

    chi_square_categorical_report(
        featured,
        categorical,
        TARGET_COLUMN,
    ).to_csv(
        REPORT_DIR / "categorical_chi_square.csv",
        index=False,
    )

    mutual_information_report(
        featured,
        numerical,
        TARGET_COLUMN,
    ).to_csv(
        REPORT_DIR / "numerical_mutual_information.csv",
        index=False,
    )

    numeric_correlation_report(
        featured,
        numerical,
        TARGET_COLUMN,
    ).to_csv(
        REPORT_DIR / "numeric_target_correlations.csv",
        index=False,
    )

    print(f"EDA artifacts saved to {REPORT_DIR.resolve()}")


if __name__ == "__main__":
    main()
