from fastapi import APIRouter,Depends
from apps.api.dependencies import get_session
from supplymind.features.dashboard.infrastructure.queries import DashboardQueryService
router=APIRouter(prefix='/dashboard',tags=['dashboard'])
@router.get('')
async def read_dashboard(s=Depends(get_session)):return await DashboardQueryService(s).summary()
