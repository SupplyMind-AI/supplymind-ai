from fastapi import APIRouter,Depends,HTTPException
from apps.api.dependencies import get_document_registry, get_semantic_search, get_settings_dependency, get_semantic_store
from apps.api.schemas import SemanticSearchRequest,DocumentIngestionRequest
from supplymind.features.knowledge.application.ingestion import IngestEnterpriseDocument
router=APIRouter(prefix='/search',tags=['semantic-search'])
@router.post('')
async def search(req:SemanticSearchRequest,svc=Depends(get_semantic_search)):return await svc.execute(req.query,top_k=req.top_k)
@router.post('/documents')
async def ingest(req:DocumentIngestionRequest,repo=Depends(get_document_registry),cfg=Depends(get_settings_dependency)):
 base=cfg.enterprise_documents_directory.resolve();path=(base/req.filename).resolve()
 if base not in path.parents:raise HTTPException(400,'Invalid document path')
 if not path.exists():raise HTTPException(404,'Document not found')
 return await IngestEnterpriseDocument(registry=repo,vector_store=get_semantic_store(),chunk_size=cfg.document_chunk_size,chunk_overlap=cfg.document_chunk_overlap).execute(path=path,namespace=cfg.pinecone_namespace_documents,source_name=req.source_name,metadata=req.metadata)
