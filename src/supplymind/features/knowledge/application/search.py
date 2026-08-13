class SemanticSearch:
 def __init__(self,*,vector_store,namespace:str,default_top_k:int=5)->None:self.vector_store=vector_store;self.namespace=namespace;self.default_top_k=default_top_k
 async def execute(self,query:str,*,top_k:int|None=None):
  if not query.strip():return []
  return await self.vector_store.search(query.strip(),namespace=self.namespace,top_k=top_k or self.default_top_k)
