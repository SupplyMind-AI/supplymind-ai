from uuid import UUID

from fastapi import APIRouter, Depends

from apps.api.dependencies import (
    get_model_registry,
    get_monitoring_repository,
    get_retraining_repository,
    get_settings_dependency,
)
from apps.api.schemas import RetrainingRequest
from supplymind.features.retraining.application.automation import (
    EvaluateRetrainingAutomation,
)
from supplymind.features.retraining.application.policy import RetrainingPolicy
from supplymind.features.retraining.application.use_cases import RequestRetraining
from supplymind.features.retraining.domain.entities import RetrainingTrigger

router = APIRouter(prefix="/retraining", tags=["retraining"])


@router.get("")
async def list_jobs(
    limit: int = 100,
    repository=Depends(get_retraining_repository),
):
    return await repository.list_recent(limit=min(max(limit, 1), 200))


@router.post("")
async def create_job(
    request: RetrainingRequest,
    repository=Depends(get_retraining_repository),
):
    return await RequestRetraining(repository).execute(
        trigger_type=RetrainingTrigger.MANUAL,
        reason=request.reason,
        base_model_version_id=(
            UUID(request.base_model_version_id)
            if request.base_model_version_id
            else None
        ),
    )


@router.post("/evaluate")
async def evaluate_automation(
    repository=Depends(get_retraining_repository),
    registry=Depends(get_model_registry),
    monitoring=Depends(get_monitoring_repository),
    settings=Depends(get_settings_dependency),
):
    policy = RetrainingPolicy(
        min_samples=settings.retraining_min_samples,
        max_psi=settings.retraining_max_psi,
        min_f1=settings.retraining_min_f1,
    )
    return await EvaluateRetrainingAutomation(
        model_registry=registry,
        monitoring_repository=monitoring,
        retraining_repository=repository,
        policy=policy,
    ).execute()
