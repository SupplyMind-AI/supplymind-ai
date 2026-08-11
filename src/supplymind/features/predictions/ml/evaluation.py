"""Binary-classification evaluation and threshold optimization."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class BinaryMetrics:
    """Metrics used for candidate comparison and monitoring."""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    average_precision: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int
    false_positive_rate: float
    false_negative_rate: float
    threshold: float

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


# -------------------
# Probabilities
# -------------------

def positive_class_probability(model, X) -> np.ndarray:
    """Return P(delayed=1) from a fitted classifier pipeline."""

    if not hasattr(model, "predict_proba"):
        raise TypeError("Classifier must implement predict_proba().")
    return model.predict_proba(X)[:, 1]


# -------------------
# Metrics
# -------------------

# -------------------
# Metrics
# -------------------

def evaluate_probabilities(
    y_true,
    probabilities,
    *,
    threshold: float,
) -> BinaryMetrics:
    """Evaluate binary predictions at a fixed probability threshold."""

    probabilities = np.asarray(probabilities)

    predictions = (
        probabilities >= threshold
    ).astype(int)

    # -------------------
    # Confusion matrix
    # -------------------

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        predictions,
        labels=[0, 1],
    ).ravel()

    # -------------------
    # Error rates
    # -------------------

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    false_negative_rate = (
        fn / (fn + tp)
        if (fn + tp) > 0
        else 0.0
    )

    # -------------------
    # Evaluation result
    # -------------------

    return BinaryMetrics(
        accuracy=float(
            accuracy_score(
                y_true,
                predictions,
            )
        ),
        precision=float(
            precision_score(
                y_true,
                predictions,
                zero_division=0,
            )
        ),
        recall=float(
            recall_score(
                y_true,
                predictions,
                zero_division=0,
            )
        ),
        f1=float(
            f1_score(
                y_true,
                predictions,
                zero_division=0,
            )
        ),
        roc_auc=float(
            roc_auc_score(
                y_true,
                probabilities,
            )
        ),
        average_precision=float(
            average_precision_score(
                y_true,
                probabilities,
            )
        ),
        true_negative=int(tn),
        false_positive=int(fp),
        false_negative=int(fn),
        true_positive=int(tp),
        false_positive_rate=float(
            false_positive_rate
        ),
        false_negative_rate=float(
            false_negative_rate
        ),
        threshold=float(threshold),
    )

    # -------------------
    # Error rates
    # -------------------

    false_positive_rate = (
        fp / (fp + tn)
        if (fp + tn) > 0
        else 0.0
    )

    false_negative_rate = (
        fn / (fn + tp)
        if (fn + tp) > 0
        else 0.0
    )

# -------------------
# Threshold optimization
# -------------------

def choose_threshold(
    y_true,
    probabilities,
    *,
    min_recall: float | None = None,
) -> tuple[float, pd.DataFrame]:
    """Choose the validation threshold that maximizes F1.

    If `min_recall` is supplied, only thresholds meeting the recall floor are
    eligible. This supports the SupplyMind business priority of avoiding
    missed delays.
    """

    rows = []

    for threshold in np.arange(0.20, 0.81, 0.01):
        metrics = evaluate_probabilities(
            y_true,
            probabilities,
            threshold=float(threshold),
        )
        rows.append(metrics.to_dict())

    table = pd.DataFrame(rows)

    eligible = table
    if min_recall is not None:
        recall_filtered = table[table["recall"] >= min_recall]
        if not recall_filtered.empty:
            eligible = recall_filtered

    winner = eligible.sort_values(
        ["f1", "recall", "precision"],
        ascending=[False, False, False],
    ).iloc[0]

    return float(winner["threshold"]), table
