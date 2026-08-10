"""Constants for the shipment-delay prediction feature."""

from __future__ import annotations

# -------------------
# Target configuration
# -------------------

TARGET_COLUMN = "is_delayed"
POSITIVE_CLASS = 1
NEGATIVE_CLASS = 0

# -------------------
# Dataset split configuration
# -------------------

TRAIN_FRACTION = 0.70
VALIDATION_FRACTION = 0.15
TEST_FRACTION = 0.15

# -------------------
# Risk thresholds
# -------------------

MEDIUM_RISK_THRESHOLD = 0.50
HIGH_RISK_THRESHOLD = 0.75

# -------------------
# Model artifact configuration
# -------------------

DEFAULT_MODEL_VERSION = "0.1.0"
MODEL_ARTIFACT_FILENAME = "model.joblib"
MODEL_METADATA_FILENAME = "metadata.json"
