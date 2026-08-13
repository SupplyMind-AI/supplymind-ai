"""Evaluate monitoring state and queue a drift-triggered retraining job if needed."""

from __future__ import annotations

import asyncio

from supplymind.features.model_registry.infrastructure.repositories import (
    SqlAlchemyModelRegistryRepository,
)
from supplymind.features.monitoring.infrastructure.repositories import (
    SqlAlchemyMonitoringRepository,
)
from supplymind.features.retraining.application.automation import (
    EvaluateRetrainingAutomation,
)
from supplymind.features.retraining.application.policy import RetrainingPolicy
from supplymind.features.retraining.infrastructure.repositories import (
    SqlAlchemyRetrainingRepository,
)
from supplymind.shared.config.settings import get_settings
from supplymind.shared.infrastructure.database.session import session_scope


async def main() -> None:
    settings = get_settings()
    policy = RetrainingPolicy(
        min_samples=settings.retraining_min_samples,
        max_psi=settings.retraining_max_psi,
        min_f1=settings.retraining_min_f1,
    )

    async with session_scope() as session:
        result = await EvaluateRetrainingAutomation(
            model_registry=SqlAlchemyModelRegistryRepository(session),
            monitoring_repository=SqlAlchemyMonitoringRepository(session),
            retraining_repository=SqlAlchemyRetrainingRepository(session),
            policy=policy,
        ).execute()
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
