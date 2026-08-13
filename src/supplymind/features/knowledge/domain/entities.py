from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime
from typing import Any
from uuid import UUID,uuid4
@dataclass(frozen=True)
class EnterpriseDocument:
    source_name:str; filename:str; checksum:str; namespace:str; status:str; chunk_count:int=0; metadata:dict[str,Any]=field(default_factory=dict); id:UUID=field(default_factory=uuid4); created_at:datetime|None=None; updated_at:datetime|None=None
@dataclass(frozen=True)
class DocumentChunk:
    id:str; document_id:str; text:str; metadata:dict[str,Any]
@dataclass(frozen=True)
class SearchHit:
    id:str; score:float; text:str; metadata:dict[str,Any]
