from fastapi import APIRouter,Depends
from apps.api.dependencies import get_model_registry, get_monitoring_repository
router=APIRouter(prefix='/monitoring',tags=['monitoring'])
@router.get('')
async def read(reg=Depends(get_model_registry),repo=Depends(get_monitoring_repository)):
 versions=await reg.list_versions('delay_prediction');champ=next((x for x in versions if x.is_champion),None) or (versions[0] if versions else None);return {'champion':champ,'snapshots':await repo.list_for_model(champ.id,limit=100) if champ else []}
