import pandas as pd

from supplymind.features.predictions.ml.features import (
    ShipmentFeatureEngineer,
    engineer_features,
)


def _frame():
    return pd.DataFrame(
        {
            "order_date": pd.to_datetime(
                ["2026-01-03 12:00", "2026-01-05 09:00"]
            ),
            "customer_city": ["Berlin", "Berlin"],
            "order_city": ["Paris", "Madrid"],
            "order_state": ["IDF", "MD"],
        }
    )


def test_feature_engineering_creates_temporal_and_frequency_features():
    result = engineer_features(_frame())

    assert "order_month" in result
    assert "order_weekday" in result
    assert "order_is_weekend" in result
    assert "customer_city_frequency" in result
    assert result["customer_city_frequency"].tolist() == [1.0, 1.0]


def test_feature_engineer_reuses_training_frequency_maps():
    train = _frame()
    validation = pd.DataFrame(
        {
            "order_date": pd.to_datetime(["2026-02-01 10:00"]),
            "customer_city": ["Unknown City"],
            "order_city": ["Paris"],
            "order_state": ["IDF"],
        }
    )

    transformer = ShipmentFeatureEngineer().fit(train)
    result = transformer.transform(validation)

    assert result.loc[0, "customer_city_frequency"] == 0.0
    assert result.loc[0, "order_city_frequency"] == 0.5
    assert result.loc[0, "order_state_frequency"] == 0.5
