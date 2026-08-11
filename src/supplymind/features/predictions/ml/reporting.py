"""Reporting and plot persistence for the ML phase."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
)


# -------------------
# File helpers
# -------------------

def ensure_directory(path: str | Path) -> Path:
    """Create and return a report directory."""

    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_json(payload: dict, path: str | Path) -> None:
    """Persist JSON with stable formatting."""

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, indent=2, default=str),
        encoding="utf-8",
    )


# -------------------
# Classification plots
# -------------------

def save_evaluation_plots(
    y_true,
    probabilities,
    threshold: float,
    output_directory: str | Path,
    prefix: str,
) -> None:
    """Persist confusion-matrix, ROC and PR plots."""

    directory = ensure_directory(output_directory)
    predictions = (np.asarray(probabilities) >= threshold).astype(int)

    ConfusionMatrixDisplay.from_predictions(
        y_true,
        predictions,
        labels=[0, 1],
        display_labels=["Not delayed", "Delayed"],
    )
    plt.title(f"{prefix} — Confusion Matrix")
    plt.tight_layout()
    plt.savefig(directory / f"{prefix}_confusion_matrix.png", dpi=150)
    plt.close()

    RocCurveDisplay.from_predictions(y_true, probabilities)
    plt.title(f"{prefix} — ROC Curve")
    plt.tight_layout()
    plt.savefig(directory / f"{prefix}_roc_curve.png", dpi=150)
    plt.close()

    PrecisionRecallDisplay.from_predictions(y_true, probabilities)
    plt.title(f"{prefix} — Precision–Recall Curve")
    plt.tight_layout()
    plt.savefig(directory / f"{prefix}_precision_recall_curve.png", dpi=150)
    plt.close()


# -------------------
# Feature importance
# -------------------

def save_feature_importance(
    model_pipeline,
    output_path: str | Path,
    *,
    top_n: int = 30,
) -> pd.DataFrame | None:
    """Persist native feature importance when the estimator exposes it."""

    preprocessor = model_pipeline.named_steps["preprocessor"]
    estimator = model_pipeline.named_steps["model"]
    feature_names = preprocessor.get_feature_names_out()

    if hasattr(estimator, "feature_importances_"):
        values = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        values = np.abs(estimator.coef_[0])
    else:
        return None

    report = (
        pd.DataFrame(
            {"feature": feature_names, "importance": values}
        )
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(destination.with_suffix(".csv"), index=False)

    plot_data = report.head(top_n).sort_values("importance")
    plot_data.plot(
        kind="barh",
        x="feature",
        y="importance",
        legend=False,
        figsize=(9, max(5, top_n * 0.25)),
        title="Top Model Features",
    )
    plt.tight_layout()
    plt.savefig(destination.with_suffix(".png"), dpi=150)
    plt.close()

    return report
