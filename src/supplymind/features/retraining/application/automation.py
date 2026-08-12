"""Deterministic retraining automation use case."""

from __future__ import annotations

from supplymind.features.retraining.application.policy import RetrainingPolicy
from supplymind.features.retraining.application.use_cases import RequestRetraining
from supplymind.features.retraining.domain.entities import RetrainingTrigger


class EvaluateRetrainingAutomation:
    """Evaluate the latest champion snapshot and queue at most one drift job."""

    def __init__(
        self,
        *,
        model_registry,
        monitoring_repository,
        retraining_repository,
        policy: RetrainingPolicy,
    ) -> None:
        self.model_registry = model_registry
        self.monitoring_repository = monitoring_repository
        self.retraining_repository = retraining_repository
        self.policy = policy

    async def execute(self, model_name: str = "delay_prediction") -> dict:
        versions = await self.model_registry.list_versions(model_name)
        champion = next((item for item in versions if item.is_champion), None)
        if champion is None:
            return {"queued": False, "reasons": ["No champion model is registered."]}

        snapshots = await self.monitoring_repository.list_for_model(
            champion.id,
            limit=1,
        )
        if not snapshots:
            return {"queued": False, "reasons": ["No monitoring snapshot exists."]}

        should_retrain, reasons = self.policy.evaluate(snapshots[0])
        if not should_retrain:
            return {"queued": False, "reasons": reasons}

        recent_jobs = await self.retraining_repository.list_recent(limit=25)
        duplicate = next(
            (
                job
                for job in recent_jobs
                if job.base_model_version_id == champion.id
                and job.status.value in {"queued", "running"}
            ),
            None,
        )
        if duplicate is not None:
            return {
                "queued": False,
                "reasons": ["A retraining job for this champion is already active."],
                "job_id": str(duplicate.id),
            }

        job = await RequestRetraining(self.retraining_repository).execute(
            trigger_type=RetrainingTrigger.DRIFT,
            reason="; ".join(reasons),
            base_model_version_id=champion.id,
            metadata={"monitoring_snapshot_id": str(snapshots[0].id)},
        )
        return {
            "queued": True,
            "reasons": reasons,
            "job_id": str(job.id),
        }
