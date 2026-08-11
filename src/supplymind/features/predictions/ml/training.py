"""Candidate-estimator factories and reusable training helpers."""

from __future__ import annotations

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from supplymind.features.predictions.ml.features import ShipmentFeatureEngineer


# -------------------
# Candidate estimators
# -------------------

def build_logistic_regression(*, random_state: int = 42):
    """Interpretable linear baseline."""

    return LogisticRegression(
        max_iter=2_000,
        class_weight="balanced",
        random_state=random_state,
    )


def build_random_forest(*, random_state: int = 42):
    """Nonlinear bagging ensemble candidate."""

    return RandomForestClassifier(
        n_estimators=300,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )


def build_xgboost(*, random_state: int = 42):
    """Boosted-tree candidate aligned with the SynDelay baseline family."""

    return XGBClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        n_jobs=-1,
    )


def build_hist_gradient_boosting(*, random_state: int = 42):
    """Optional sklearn-native boosting candidate."""

    return HistGradientBoostingClassifier(
        learning_rate=0.08,
        max_iter=300,
        max_leaf_nodes=31,
        l2_regularization=0.1,
        random_state=random_state,
    )


# -------------------
# Pipeline training
# -------------------

def fit_pipeline(preprocessor, estimator, X, y) -> Pipeline:
    """Fit feature engineering, preprocessing, and estimator as one artifact."""

    pipeline = Pipeline(
        [
            ("feature_engineering", ShipmentFeatureEngineer()),
            ("preprocessor", preprocessor),
            ("model", estimator),
        ]
    )
    pipeline.fit(X, y)
    return pipeline
