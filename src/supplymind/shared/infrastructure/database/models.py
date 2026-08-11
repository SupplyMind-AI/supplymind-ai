"""Import all ORM models so Alembic can discover shared metadata.

Keep this module infrastructure-only. Domain and application code must not import it.
"""

from supplymind.features.events.infrastructure.models import EventModel
from supplymind.features.model_registry.infrastructure.models import ModelVersionModel
from supplymind.features.monitoring.infrastructure.models import MonitoringSnapshotModel
from supplymind.features.predictions.infrastructure.models import PredictionModel
from supplymind.features.retraining.infrastructure.models import RetrainingJobModel
from supplymind.features.shipments.infrastructure.models import ShipmentModel

__all__ = [
    "EventModel",
    "ModelVersionModel",
    "MonitoringSnapshotModel",
    "PredictionModel",
    "RetrainingJobModel",
    "ShipmentModel",
]
