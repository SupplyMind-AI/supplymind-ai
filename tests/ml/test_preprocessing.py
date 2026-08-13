import pandas as pd

from supplymind.features.predictions.ml.preprocessing import build_preprocessor


def test_one_hot_encoder_handles_unseen_categories():
    train = pd.DataFrame({"num": [1.0, 2.0], "cat": ["A", "B"]})
    test = pd.DataFrame({"num": [3.0], "cat": ["C"]})

    preprocessor = build_preprocessor(
        ["num"],
        ["cat"],
        scale_numerical=True,
    )

    preprocessor.fit(train)
    transformed = preprocessor.transform(test)

    assert transformed.shape[0] == 1
