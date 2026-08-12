from fastapi import APIRouter,Depends
from apps.api.dependencies import get_weather_service
router=APIRouter(prefix='/weather',tags=['weather'])
@router.get('')
async def risk(location:str,svc=Depends(get_weather_service)):return await svc.execute(location=location)
