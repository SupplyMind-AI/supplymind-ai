"""Candidate-estimator factories and reusable training helpers."""

from __future__ import annotations

from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier


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
    """Nonlinear ensemble candidate with robust tabular performance."""

    return RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )


def build_xgboost(*, random_state: int = 42):
    """Boosted-tree candidate aligned with the SynDelay benchmark family."""

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
    """Optional fourth sklearn-native boosting candidate."""

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
    """Fit preprocessing and estimator as one serving artifact."""

    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("model", estimator),
        ]
    )
    pipeline.fit(X, y)
    return pipeline
