from __future__ import annotations
import hashlib
from pathlib import Path
from supplymind.features.knowledge.domain.entities import EnterpriseDocument,DocumentChunk
from supplymind.features.knowledge.infrastructure.document_loader import load_document_text
from supplymind.features.knowledge.infrastructure.chunking import chunk_text
class IngestEnterpriseDocument:
 def __init__(self,*,registry,vector_store,chunk_size:int,chunk_overlap:int)->None:self.registry=registry;self.vector_store=vector_store;self.chunk_size=chunk_size;self.chunk_overlap=chunk_overlap
 async def execute(self,*,path:str|Path,namespace:str,source_name:str='enterprise',metadata:dict|None=None):
  p=Path(path);checksum=hashlib.sha256(p.read_bytes()).hexdigest();existing=await self.registry.get_by_checksum(checksum)
  if existing and existing.status=='indexed':return existing
  d=existing or await self.registry.add(EnterpriseDocument(source_name=source_name,filename=p.name,checksum=checksum,namespace=namespace,status='indexing',metadata=metadata or {}));texts=chunk_text(load_document_text(p),chunk_size=self.chunk_size,overlap=self.chunk_overlap);chunks=[DocumentChunk(id=f'{d.id}#{i:05d}',document_id=str(d.id),text=t,metadata={'filename':d.filename,'source_name':source_name,'chunk_index':i,**(metadata or {})}) for i,t in enumerate(texts)];count=await self.vector_store.upsert(chunks,namespace=namespace);return await self.registry.update_status(d.id,status='indexed',chunk_count=count)
