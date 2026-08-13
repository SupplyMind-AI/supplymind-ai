from __future__ import annotations
import json
from typing import Literal
from langchain_openai import ChatOpenAI
from langgraph.graph import END,START,StateGraph
from langsmith import traceable
from supplymind.features.assistant.application.routing import route_query
from supplymind.features.assistant.domain.schemas import AssistantAnswer,AssistantRequest
from supplymind.features.assistant.domain.state import AssistantState
SYSTEM = """You are the SupplyMind operational assistant. Answer only from supplied context. Never invent shipment facts, model outputs, weather, events, document content or causal explanations. A model prediction is delay risk, not proof of cause. Weather and events are possible context only. If evidence is insufficient, say what is missing. Cite only supplied source IDs. Be concise and operational."""
class SupplyMindAssistant:
 def __init__(self,*,tools:dict,model:str,api_key:str|None=None)->None:
  self.tools=tools;llm=ChatOpenAI(model=model,api_key=api_key,temperature=0);self.answer_llm=llm.with_structured_output(AssistantAnswer,method='json_schema');self.graph=self._build_graph()
 def _build_graph(self):
  b=StateGraph(AssistantState)
  for name,fn in [('route',self._route),('shipment',self._shipment),('weather',self._weather),('events',self._events),('knowledge',self._knowledge),('combined',self._combined),('answer',self._answer)]:b.add_node(name,fn)
  b.add_edge(START,'route');b.add_conditional_edges('route',self._next,{'shipment':'shipment','weather':'weather','events':'events','knowledge':'knowledge','combined':'combined'})
  for n in ['shipment','weather','events','knowledge','combined']:b.add_edge(n,'answer')
  b.add_edge('answer',END);return b.compile()
 async def _route(self,state):return {'intent':route_query(state['query'],shipment_external_id=state.get('shipment_external_id'),location=state.get('location')),'context':[]}
 @staticmethod
 def _next(state)->Literal['shipment','weather','events','knowledge','combined']:return state['intent']
 async def _shipment(self,state):
  x=state.get('shipment_external_id');r=await self.tools['shipment_context'].ainvoke({'external_id':x}) if x else None
  return {'context':[] if r is None else [{'source_id':f'shipment:{x}','source_type':'shipment','label':x,'content':r}]}
 async def _weather(self,state):
  x=state.get('location');r=await self.tools['weather_context'].ainvoke({'location':x}) if x else None
  return {'context':[] if r is None else [{'source_id':f'weather:{x}','source_type':'weather','label':x,'content':r}]}
 async def _events(self,state):
  r=await self.tools['active_events'].ainvoke({'limit':50});return {'context':[{'source_id':'events:active','source_type':'events','label':'Active supply-chain events','content':r}]}
 async def _knowledge(self,state):
  r=await self.tools['search_enterprise_knowledge'].ainvoke({'query':state['query'],'top_k':5});return {'context':[{'source_id':f"doc:{x['id']}",'source_type':'document','label':x.get('metadata',{}).get('filename',x['id']),'content':x['text'],'score':x['score']} for x in r]}
 async def _combined(self,state):
  c=[];x=state.get('shipment_external_id');loc=state.get('location')
  if x:
   r=await self.tools['shipment_context'].ainvoke({'external_id':x});c.append({'source_id':f'shipment:{x}','source_type':'shipment','label':x,'content':r});payload=(r.get('shipment') or {}).get('payload') or {};loc=loc or payload.get('order_city') or payload.get('customer_city') or payload.get('order_country')
  if loc:
   try:r=await self.tools['weather_context'].ainvoke({'location':str(loc)});c.append({'source_id':f'weather:{loc}','source_type':'weather','label':str(loc),'content':r})
   except Exception as exc:c.append({'source_id':'weather:unavailable','source_type':'weather','label':'Weather unavailable','content':{'error':str(exc)}})
  e=await self.tools['active_events'].ainvoke({'limit':30});c.append({'source_id':'events:active','source_type':'events','label':'Active supply-chain events','content':e})
  d=await self.tools['search_enterprise_knowledge'].ainvoke({'query':state['query'],'top_k':3});c.extend({'source_id':f"doc:{i['id']}",'source_type':'document','label':i.get('metadata',{}).get('filename',i['id']),'content':i['text'],'score':i['score']} for i in d);return {'context':c}
 async def _answer(self,state):
  c=state.get('context') or [];r=await self.answer_llm.ainvoke(f"{SYSTEM}\nQuestion: {state['query']}\nContext JSON: {json.dumps(c,default=str)}");allowed={i['source_id'] for i in c if i.get('source_id')};r=r.model_copy(update={'citations':[x for x in r.citations if x.source_id in allowed]})
  if not c:r=r.model_copy(update={'confidence':'low','citations':[],'limitations':[ *r.limitations,'No grounded SupplyMind context was available.']})
  return {'answer':r.model_dump(mode='json')}
 @traceable(name='supplymind-assistant')
 async def ask(self,request:AssistantRequest)->AssistantAnswer:
  r=await self.graph.ainvoke({'query':request.query,'shipment_external_id':request.shipment_external_id,'location':request.location});return AssistantAnswer.model_validate(r['answer'])
