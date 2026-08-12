from __future__ import annotations
from typing import Literal
from pydantic import BaseModel,Field
AssistantIntent=Literal['shipment','weather','events','knowledge','combined']
class AssistantRequest(BaseModel):
 query:str=Field(min_length=2);shipment_external_id:str|None=None;location:str|None=None
class AssistantCitation(BaseModel):
 source_id:str;source_type:str;label:str
class AssistantAnswer(BaseModel):
 answer:str;citations:list[AssistantCitation]=[];confidence:Literal['high','medium','low'];limitations:list[str]=[]
