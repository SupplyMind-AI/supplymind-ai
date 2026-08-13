"""New-shipment prediction orchestration."""
from __future__ import annotations
from supplymind.features.model_registry.domain.entities import ModelVersion
from supplymind.features.predictions.domain.risk import decision_explanation


class PredictShipment:
    def __init__(self, *, runtime, create_shipment, record_prediction, model_registry):
        self.runtime = runtime
        self.create_shipment = create_shipment
        self.record_prediction = record_prediction
        self.model_registry = model_registry

    async def execute(self, *, external_id, order_date, features, source="manual"):
        shipment = await self.create_shipment.execute(
            external_id=external_id,
            order_date=order_date,
            source=source,
            status="predicted",
            payload=features,
        )
        result = self.runtime.predict(features)
        model_version = await self._ensure_model_registered()
        prediction = await self.record_prediction.execute(
            shipment_id=shipment.id,
            model_version_id=model_version.id,
            delayed=result["delayed"],
            delay_probability=result["delay_probability"],
            threshold=result["threshold"],
            risk_level=result["risk_level"],
        )
        return {
            "shipment_id": str(shipment.id),
            "prediction_id": str(prediction.id),
            "external_id": shipment.external_id,
            **result,
            "decision_explanation": decision_explanation(
                result["delay_probability"], result["threshold"]
            ),
        }

    async def _ensure_model_registered(self):
        existing = await self.model_registry.get_by_name_version(
            self.runtime.model_name, self.runtime.model_version
        )
        if existing is not None:
            return await self.model_registry.promote(existing.id) if not existing.is_champion else existing
        model = await self.model_registry.add(
            ModelVersion(
                name=self.runtime.model_name,
                version=self.runtime.model_version,
                artifact_uri="models/champion",
                target_column="is_delayed",
                threshold=self.runtime.threshold,
                metrics=self.runtime.metadata.get("test_metrics", {}),
                feature_columns=self.runtime.metadata.get("feature_columns", []),
                trained_at=None,
                is_champion=False,
            )
        )
        return await self.model_registry.promote(model.id)
