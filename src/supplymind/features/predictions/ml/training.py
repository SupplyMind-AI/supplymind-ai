"""Candidate model construction and training."""

from __future__ import annotations

from typing import Any

from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier


# -------------------
# Candidate models
# -------------------

def build_candidate_estimators(
    *,
    random_state: int = 42,
) -> dict[str, ClassifierMixin]:
    """Return the approved V1 candidate estimators."""

    return {
        "logistic_regression": LogisticRegression(
            max_iter=1_000,
            class_weight="balanced",
            random_state=random_state,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        ),
        "xgboost": XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state,
            n_jobs=-1,
        ),
    }


# -------------------
# Training pipeline
# -------------------

def train_pipeline(
    preprocessor: Any,
    estimator: ClassifierMixin,
    features,
    target,
) -> Pipeline:
    """Fit preprocessing and estimator as one persisted pipeline."""

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", estimator),
        ]
    )
    pipeline.fit(features, target)
    return pipeline
