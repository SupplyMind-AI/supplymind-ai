import pandas as pd

from supplymind.features.predictions.application.dataset import (
    add_canonical_targets,
    excel_serial_to_datetime,
)
from supplymind.features.predictions.application.validation import (
    validate_target_consistency,
)


# -------------------
# Canonical target creation
# -------------------

def test_canonical_targets_merge_early_and_on_time():
    frame = pd.DataFrame({"label": [0, 1, 2, 2]})

    result = add_canonical_targets(frame)

    assert result["delivery_outcome"].tolist() == [0, 1, 2, 2]
    assert result["is_delayed"].tolist() == [0, 0, 1, 1]


# -------------------
# Target consistency
# -------------------

def test_target_consistency_accepts_valid_mapping():
    frame = pd.DataFrame(
        {
            "label": [0, 1, 2, 2],
            "delivery_outcome": [0, 1, 2, 2],
            "is_delayed": [0, 0, 1, 1],
        }
    )

    result = validate_target_consistency(frame)

    assert result.is_valid
    assert result.errors == []


def test_target_consistency_rejects_invalid_mapping():
    frame = pd.DataFrame(
        {
            "label": [0, 1, 2],
            "delivery_outcome": [0, 1, 2],
            "is_delayed": [0, 1, 1],
        }
    )

    result = validate_target_consistency(frame)

    assert not result.is_valid


# -------------------
# Excel serial date conversion
# -------------------

def test_excel_serial_date_conversion():
    result = excel_serial_to_datetime(pd.Series([42005.0]))

    assert result.iloc[0].year == 2015
