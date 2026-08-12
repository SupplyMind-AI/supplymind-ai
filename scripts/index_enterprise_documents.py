"""Index all supported files from data/enterprise_documents."""
from __future__ import annotations
import asyncio
from supplymind.features.knowledge.application.ingestion import IngestEnterpriseDocument
from supplymind.features.knowledge.infrastructure.document_loader import SUPPORTED_SUFFIXES
from supplymind.features.knowledge.infrastructure.repositories import SqlAlchemyDocumentRegistryRepository
from supplymind.features.knowledge.infrastructure.vector_store import PineconeSemanticStore
from supplymind.shared.config.settings import get_settings
from supplymind.shared.infrastructure.database.session import session_scope
async def main():
 cfg=get_settings();cfg.enterprise_documents_directory.mkdir(parents=True,exist_ok=True);store=PineconeSemanticStore(pinecone_api_key=cfg.pinecone_api_key or '',index_host=cfg.pinecone_index_host or '',embedding_model=cfg.embedding_model,openai_api_key=cfg.openai_api_key)
 async with session_scope() as s:
  use=IngestEnterpriseDocument(registry=SqlAlchemyDocumentRegistryRepository(s),vector_store=store,chunk_size=cfg.document_chunk_size,chunk_overlap=cfg.document_chunk_overlap)
  for p in sorted(cfg.enterprise_documents_directory.iterdir()):
   if p.suffix.lower() in SUPPORTED_SUFFIXES:
    d=await use.execute(path=p,namespace=cfg.pinecone_namespace_documents);print(f'{d.filename}: {d.status}, {d.chunk_count} chunks')
if __name__=='__main__':asyncio.run(main())
