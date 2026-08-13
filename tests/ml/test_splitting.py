import pandas as pd

from supplymind.features.predictions.ml.splitting import temporal_split


def test_temporal_split_preserves_order():
    frame = pd.DataFrame(
        {
            "order_date": pd.date_range("2026-01-01", periods=100),
            "value": range(100),
        }
    )

    split = temporal_split(frame, "order_date")

    assert len(split.train) == 70
    assert len(split.validation) == 15
    assert len(split.test) == 15
    assert split.train["order_date"].max() <= split.validation["order_date"].min()
    assert split.validation["order_date"].max() <= split.test["order_date"].min()
