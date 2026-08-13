"""Feature-selection diagnostics inspired by the reference notebook.

The production feature contract remains domain-driven first. Statistical
methods are used to understand and validate candidate features, not to let a
single sample silently redefine the API contract.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import OrdinalEncoder


# -------------------
# Chi-square analysis
# -------------------

def chi_square_categorical_report(
    frame: pd.DataFrame,
    categorical_features: list[str],
    target_column: str,
) -> pd.DataFrame:
    """Measure categorical association with the binary target."""

    rows: list[dict[str, float | str | int]] = []

    for column in categorical_features:
        table = pd.crosstab(frame[column], frame[target_column])
        chi2, p_value, dof, _ = chi2_contingency(table)

        rows.append(
            {
                "feature": column,
                "chi2": float(chi2),
                "p_value": float(p_value),
                "degrees_of_freedom": int(dof),
                "significant_at_0_05": bool(p_value < 0.05),
            }
        )

    return pd.DataFrame(rows).sort_values("p_value").reset_index(drop=True)


# -------------------
# Mutual information
# -------------------

def mutual_information_report(
    frame: pd.DataFrame,
    numerical_features: list[str],
    target_column: str,
    *,
    random_state: int = 42,
) -> pd.DataFrame:
    """Estimate nonlinear information shared with the target."""

    X = frame[numerical_features].copy()
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median(numeric_only=True))

    scores = mutual_info_classif(
        X,
        frame[target_column],
        random_state=random_state,
    )

    return (
        pd.DataFrame(
            {"feature": numerical_features, "mutual_information": scores}
        )
        .sort_values("mutual_information", ascending=False)
        .reset_index(drop=True)
    )


# -------------------
# Correlation report
# -------------------

def numeric_correlation_report(
    frame: pd.DataFrame,
    numerical_features: list[str],
    target_column: str,
) -> pd.DataFrame:
    """Return absolute Pearson correlations with the binary target."""

    selected = frame[numerical_features + [target_column]].copy()
    correlations = (
        selected.corr(numeric_only=True)[target_column]
        .drop(target_column)
        .sort_values(key=lambda s: s.abs(), ascending=False)
    )

    return (
        correlations.rename("correlation")
        .reset_index()
        .rename(columns={"index": "feature"})
    )