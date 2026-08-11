import numpy as np

from supplymind.features.predictions.ml.evaluation import (
    evaluate_probabilities,
)


# -------------------
# Confusion-matrix counts
# -------------------

def test_evaluation_includes_confusion_matrix_counts():
    y_true = np.array(
        [0, 0, 0, 1, 1, 1]
    )

    probabilities = np.array(
        [0.10, 0.20, 0.90, 0.80, 0.70, 0.10]
    )

    metrics = evaluate_probabilities(
        y_true,
        probabilities,
        threshold=0.50,
    )

    assert metrics.true_negative == 2
    assert metrics.false_positive == 1
    assert metrics.false_negative == 1
    assert metrics.true_positive == 2


# -------------------
# Error rates
# -------------------

def test_evaluation_calculates_error_rates():
    y_true = np.array(
        [0, 0, 0, 1, 1, 1]
    )

    probabilities = np.array(
        [0.10, 0.20, 0.90, 0.80, 0.70, 0.10]
    )

    metrics = evaluate_probabilities(
        y_true,
        probabilities,
        threshold=0.50,
    )

    assert metrics.false_positive_rate == 1 / 3
    assert metrics.false_negative_rate == 1 / 3