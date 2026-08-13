"""Train all V1 candidate models and select a champion."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import time

import pandas as pd

from supplymind.features.predictions.domain.constants import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)
from supplymind.features.predictions.ml.artifacts import save_model_artifact
from supplymind.features.predictions.ml.evaluation import (
    choose_threshold,
    evaluate_probabilities,
    positive_class_probability,
)
from supplymind.features.predictions.ml.preprocessing import build_preprocessor
from supplymind.features.predictions.ml.reporting import (
    save_evaluation_plots,
    save_feature_importance,
    save_json,
)
from supplymind.features.predictions.ml.training import (
    build_hist_gradient_boosting,
    build_logistic_regression,
    build_random_forest,
    build_xgboost,
    fit_pipeline,
)
from supplymind.features.predictions.ml.workflow import (
    load_clean_syndelay,
    prepare_model_data,
)


DATASET_PATH = Path("data/raw/syndelay/syndelay_v1.csv")
REPORT_DIR = Path("reports/models")
MODEL_DIR = Path("models")


def _train_candidate(
    name,
    estimator,
    data,
    *,
    scale_numerical,
    sparse_output=True,
):
    preprocessor = build_preprocessor(
        NUMERICAL_FEATURES,
        CATEGORICAL_FEATURES,
        scale_numerical=scale_numerical,
        sparse_output=sparse_output,
    )

    started = time.perf_counter()
    model = fit_pipeline(
        preprocessor,
        estimator,
        data.X_train,
        data.y_train,
    )
    training_seconds = time.perf_counter() - started

    validation_probability = positive_class_probability(
        model,
        data.X_validation,
    )
    threshold, threshold_table = choose_threshold(
        data.y_validation,
        validation_probability,
    )
    metrics = evaluate_probabilities(
        data.y_validation,
        validation_probability,
        threshold=threshold,
    )

    candidate_report_dir = REPORT_DIR / name
    candidate_report_dir.mkdir(parents=True, exist_ok=True)

    threshold_table.to_csv(
        candidate_report_dir / "threshold_search.csv",
        index=False,
    )
    save_json(
        {
            **metrics.to_dict(),
            "training_seconds": training_seconds,
        },
        candidate_report_dir / "validation_metrics.json",
    )
    save_evaluation_plots(
        data.y_validation,
        validation_probability,
        threshold,
        candidate_report_dir,
        "validation",
    )
    save_feature_importance(
        model,
        candidate_report_dir / "feature_importance",
    )

    save_model_artifact(
        model,
        {
            "model_name": name,
            "model_version": "0.1.0-candidate",
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "threshold": threshold,
            "validation_metrics": metrics.to_dict(),
            "training_seconds": training_seconds,
        },
        MODEL_DIR / "candidates" / name,
    )

    return {
        "model_name": name,
        **metrics.to_dict(),
        "training_seconds": training_seconds,
    }


def main() -> None:
    frame = load_clean_syndelay(DATASET_PATH)
    data = prepare_model_data(frame)

    candidates = [
        ("logistic_regression", build_logistic_regression(), True, True),
        ("random_forest", build_random_forest(), False, True),
        ("xgboost", build_xgboost(), False, True),
        # HistGradientBoosting requires dense input.
        ("hist_gradient_boosting", build_hist_gradient_boosting(), True, False),
    ]

    results = []

    for name, estimator, scale, sparse in candidates:
        print(f"Training {name}...")
        results.append(
            _train_candidate(
                name,
                estimator,
                data,
                scale_numerical=scale,
                sparse_output=sparse,
            )
        )

    comparison = pd.DataFrame(results).sort_values(
        ["f1", "recall", "roc_auc"],
        ascending=[False, False, False],
    )
    comparison.to_csv(REPORT_DIR / "model_comparison.csv", index=False)

    winner_name = comparison.iloc[0]["model_name"]
    print(f"Validation champion: {winner_name}")

    # Champion is refit on train + validation only after model selection.
    estimator_map = {
        "logistic_regression": (build_logistic_regression(), True, True),
        "random_forest": (build_random_forest(), False, True),
        "xgboost": (build_xgboost(), False, True),
        "hist_gradient_boosting": (build_hist_gradient_boosting(), True, False),
    }
    estimator, scale, sparse = estimator_map[winner_name]

    X_train_validation = pd.concat(
        [data.X_train, data.X_validation],
        ignore_index=True,
    )
    y_train_validation = pd.concat(
        [data.y_train, data.y_validation],
        ignore_index=True,
    )

    preprocessor = build_preprocessor(
        NUMERICAL_FEATURES,
        CATEGORICAL_FEATURES,
        scale_numerical=scale,
        sparse_output=sparse,
    )
    champion = fit_pipeline(
        preprocessor,
        estimator,
        X_train_validation,
        y_train_validation,
    )

    threshold = float(comparison.iloc[0]["threshold"])
    test_probability = positive_class_probability(
        champion,
        data.X_test,
    )
    test_metrics = evaluate_probabilities(
        data.y_test,
        test_probability,
        threshold=threshold,
    )

    champion_report = REPORT_DIR / "champion"
    champion_report.mkdir(parents=True, exist_ok=True)
    save_json(
        test_metrics.to_dict(),
        champion_report / "test_metrics.json",
    )
    save_evaluation_plots(
        data.y_test,
        test_probability,
        threshold,
        champion_report,
        "test",
    )
    save_feature_importance(
        champion,
        champion_report / "feature_importance",
    )

    save_model_artifact(
        champion,
        {
            "model_name": winner_name,
            "model_version": "1.0.0",
            "trained_at": datetime.now(timezone.utc).isoformat(),
            "threshold": threshold,
            "selection_metric": "validation_f1_then_recall_then_roc_auc",
            "validation_metrics": comparison.iloc[0].to_dict(),
            "test_metrics": test_metrics.to_dict(),
            "source_dataset": "SynDelay v1",
            "target": {
                "source_column": "label",
                "canonical_column": "is_delayed",
                "mapping": {
                    "0_early": 0,
                    "1_on_time": 0,
                    "2_delayed": 1,
                },
            },
        },
        MODEL_DIR / "champion",
    )

    print("Champion saved to models/champion/")


if __name__ == "__main__":
    main()
