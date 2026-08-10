"""Scikit-learn preprocessing pipeline construction."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# -------------------
# Preprocessing pipeline
# -------------------

def build_preprocessor(
    numerical_features: list[str],
    categorical_features: list[str],
    *,
    scale_numerical: bool = True,
) -> ColumnTransformer:
    """Build one reusable preprocessing contract for all candidate models."""

    numerical_steps: list[tuple[str, object]] = [
        ("imputer", SimpleImputer(strategy="median")),
    ]
    if scale_numerical:
        numerical_steps.append(("scaler", StandardScaler()))

    numerical_pipeline = Pipeline(steps=numerical_steps)

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numerical", numerical_pipeline, numerical_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )
