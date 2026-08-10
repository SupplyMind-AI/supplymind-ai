"""Consistent binary-classification evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


# -------------------
# Evaluation result
# -------------------

@dataclass(frozen=True)
class BinaryClassificationMetrics:
    """Metrics used to compare and monitor delay models."""

    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    true_negative: int
    false_positive: int
    false_negative: int
    true_positive: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


# -------------------
# Model evaluation
# -------------------

def evaluate_binary_classifier(
    model,
    features,
    target,
    *,
    threshold: float = 0.50,
) -> BinaryClassificationMetrics:
    """Evaluate a fitted binary classifier using one threshold."""

    probabilities = model.predict_proba(features)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        target,
        predictions,
        labels=[0, 1],
    ).ravel()

    return BinaryClassificationMetrics(
        accuracy=float(accuracy_score(target, predictions)),
        precision=float(
            precision_score(target, predictions, zero_division=0)
        ),
        recall=float(recall_score(target, predictions, zero_division=0)),
        f1=float(f1_score(target, predictions, zero_division=0)),
        roc_auc=float(roc_auc_score(target, probabilities)),
        true_negative=int(tn),
        false_positive=int(fp),
        false_negative=int(fn),
        true_positive=int(tp),
    )
