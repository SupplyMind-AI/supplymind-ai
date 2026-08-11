"""Reusable scikit-learn preprocessing builders."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# -------------------
# Shared preprocessing
# -------------------

def build_preprocessor(
    numerical_features: list[str],
    categorical_features: list[str],
    *,
    scale_numerical: bool,
) -> ColumnTransformer:
    """Build a model-safe preprocessing transformer.

    Categorical values are one-hot encoded with unknown-category tolerance.
    Numerical values are median-imputed and optionally standardized.
    """

    numeric_steps: list[tuple[str, object]] = [
        ("imputer", SimpleImputer(strategy="median")),
    ]

    if scale_numerical:
        numeric_steps.append(("scaler", StandardScaler()))

    numeric_pipeline = Pipeline(numeric_steps)

    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "one_hot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=True,
                    min_frequency=10,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        [
            ("numerical", numeric_pipeline, numerical_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


# -------------------
# Feature names
# -------------------

def transformed_feature_names(fitted_preprocessor) -> list[str]:
    """Return post-encoding feature names from a fitted transformer."""

    return fitted_preprocessor.get_feature_names_out().tolist()
