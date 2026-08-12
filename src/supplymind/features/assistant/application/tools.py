from datetime import datetime,timezone
from langchain.tools import tool

def build_assistant_tools(*,shipment_repository,prediction_repository,event_repository,weather_service,semantic_search):
 @tool
 async def shipment_context(external_id:str)->dict:
  """Get one shipment and its latest persisted prediction."""
  s=await shipment_repository.get_by_external_id(external_id)
  if not s:return {'found':False,'external_id':external_id}
  p=await prediction_repository.get_latest_for_shipment(s.id)
  return {'found':True,'shipment':{'id':str(s.id),'external_id':s.external_id,'order_date':s.order_date.isoformat(),'source':s.source,'status':s.status,'payload':s.payload},'prediction':({'delayed':p.delayed,'delay_probability':p.delay_probability,'threshold':p.threshold,'risk_level':p.risk_level,'model_version_id':str(p.model_version_id)} if p else None)}
 @tool
 async def weather_context(location:str)->dict:
  """Get forecast-derived shipment weather risk for a location."""
  return (await weather_service.execute(location=location)).model_dump(mode='json')
 @tool
 async def active_events(limit:int=50)->list[dict]:
  """List active supply-chain disruption events."""
  es=await event_repository.list_active(at=datetime.now(timezone.utc),limit=min(max(limit,1),100))
  return [{'id':str(e.id),'source':e.source,'event_type':e.event_type,'title':e.title,'description':e.description,'severity':e.severity,'country':e.country,'region':e.region,'latitude':e.latitude,'longitude':e.longitude,'starts_at':e.starts_at.isoformat() if e.starts_at else None,'ends_at':e.ends_at.isoformat() if e.ends_at else None} for e in es]
 @tool
 async def search_enterprise_knowledge(query:str,top_k:int=5)->list[dict]:
  """Semantically search indexed enterprise documents."""
  hs=await semantic_search.execute(query,top_k=min(max(top_k,1),10));return [{'id':h.id,'score':h.score,'text':h.text,'metadata':h.metadata} for h in hs]
 return {'shipment_context':shipment_context,'weather_context':weather_context,'active_events':active_events,'search_enterprise_knowledge':search_enterprise_knowledge}
