from fastapi import APIRouter,Depends,HTTPException
from apps.api.dependencies import get_shipment_repository
router=APIRouter(prefix='/shipments',tags=['shipments'])
@router.get('')
async def list_items(limit:int=50,repo=Depends(get_shipment_repository)):
 return [{'id':str(x.id),'external_id':x.external_id,'order_date':x.order_date,'source':x.source,'status':x.status,'payload':x.payload} for x in await repo.list_recent(limit=min(max(limit,1),200),offset=0)]
@router.get('/{external_id}')
async def get_item(external_id:str,repo=Depends(get_shipment_repository)):
 x=await repo.get_by_external_id(external_id)
 if not x:raise HTTPException(404,'Shipment not found')
 return {'id':str(x.id),'external_id':x.external_id,'order_date':x.order_date,'source':x.source,'status':x.status,'payload':x.payload}
