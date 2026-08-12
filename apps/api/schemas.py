from datetime import datetime
from typing import Any
from pydantic import BaseModel,Field
class PredictionRequest(BaseModel):external_id:str=Field(min_length=1,max_length=128);order_date:datetime;features:dict[str,Any]
class SemanticSearchRequest(BaseModel):query:str=Field(min_length=2);top_k:int=Field(default=5,ge=1,le=20)
class DocumentIngestionRequest(BaseModel):filename:str;source_name:str='enterprise';metadata:dict[str,Any]={}
class RetrainingRequest(BaseModel):reason:str=Field(min_length=3);base_model_version_id:str|None=None
