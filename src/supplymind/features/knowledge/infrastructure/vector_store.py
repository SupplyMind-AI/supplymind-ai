from __future__ import annotations
import asyncio
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone
from supplymind.features.knowledge.domain.entities import DocumentChunk,SearchHit
class PineconeSemanticStore:
 def __init__(self,*,pinecone_api_key:str,index_host:str,embedding_model:str,openai_api_key:str|None=None)->None:
  if not pinecone_api_key or not index_host: raise ValueError('Pinecone credentials/host required.')
  self.index=Pinecone(api_key=pinecone_api_key).Index(host=index_host);self.embeddings=OpenAIEmbeddings(model=embedding_model,api_key=openai_api_key)
 async def upsert(self,chunks:list[DocumentChunk],*,namespace:str,batch_size:int=100)->int:
  if not chunks:return 0
  vectors=await self.embeddings.aembed_documents([x.text for x in chunks]);records=[{'id':c.id,'values':v,'metadata':{**c.metadata,'text':c.text,'document_id':c.document_id}} for c,v in zip(chunks,vectors,strict=True)]
  for i in range(0,len(records),batch_size): await asyncio.to_thread(self.index.upsert,vectors=records[i:i+batch_size],namespace=namespace)
  return len(records)
 async def search(self,query:str,*,namespace:str,top_k:int=5,metadata_filter:dict|None=None)->list[SearchHit]:
  v=await self.embeddings.aembed_query(query);r=await asyncio.to_thread(self.index.query,vector=v,top_k=top_k,include_metadata=True,include_values=False,namespace=namespace,filter=metadata_filter)
  out=[]
  for m in getattr(r,'matches',None) or []:
   md=dict(getattr(m,'metadata',None) or {});out.append(SearchHit(id=str(m.id),score=float(m.score),text=str(md.pop('text','')),metadata=md))
  return out
