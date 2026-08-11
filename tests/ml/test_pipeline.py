import pandas as pd
from sklearn.linear_model import LogisticRegression

from supplymind.features.predictions.ml.preprocessing import build_preprocessor
from supplymind.features.predictions.ml.training import fit_pipeline


def test_fitted_pipeline_contains_feature_engineering_state():
    X = pd.DataFrame(
        {
            "order_date": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
            ),
            "customer_city": ["A", "A", "B", "B"],
            "order_city": ["C", "C", "D", "D"],
            "order_state": ["E", "E", "F", "F"],
            "num": [1.0, 2.0, 3.0, 4.0],
            "cat": ["x", "y", "x", "y"],
        }
    )
    y = pd.Series([0, 0, 1, 1])

    preprocessor = build_preprocessor(
        numerical_features=["num", "order_month", "customer_city_frequency"],
        categorical_features=["cat"],
        scale_numerical=True,
    )

    model = fit_pipeline(
        preprocessor,
        LogisticRegression(),
        X,
        y,
    )

    feature_engineer = model.named_steps["feature_engineering"]
    assert hasattr(feature_engineer, "frequency_maps_")
    assert model.predict_proba(X).shape == (4, 2)
