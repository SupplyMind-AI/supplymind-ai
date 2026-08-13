from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from supplymind.features.knowledge.domain.entities import EnterpriseDocument
from supplymind.features.knowledge.domain.repositories import DocumentRegistryRepository
from supplymind.features.knowledge.infrastructure.models import EnterpriseDocumentModel

def to_entity(m): return EnterpriseDocument(id=m.id,source_name=m.source_name,filename=m.filename,checksum=m.checksum,namespace=m.namespace,status=m.status,chunk_count=m.chunk_count,metadata=m.document_metadata or {},created_at=m.created_at,updated_at=m.updated_at)
class SqlAlchemyDocumentRegistryRepository(DocumentRegistryRepository):
 def __init__(self,session:AsyncSession)->None:self.session=session
 async def add(self,d):
  m=EnterpriseDocumentModel(id=d.id,source_name=d.source_name,filename=d.filename,checksum=d.checksum,namespace=d.namespace,status=d.status,chunk_count=d.chunk_count,document_metadata=d.metadata);self.session.add(m);await self.session.flush();await self.session.refresh(m);return to_entity(m)
 async def get_by_checksum(self,checksum):
  m=(await self.session.execute(select(EnterpriseDocumentModel).where(EnterpriseDocumentModel.checksum==checksum))).scalar_one_or_none();return to_entity(m) if m else None
 async def update_status(self,document_id:UUID,*,status:str,chunk_count:int):
  m=await self.session.get(EnterpriseDocumentModel,document_id)
  if not m: raise LookupError(f'Document not found: {document_id}')
  m.status=status;m.chunk_count=chunk_count;await self.session.flush();await self.session.refresh(m);return to_entity(m)
 async def list_recent(self,*,limit:int=100):
  rows=(await self.session.execute(select(EnterpriseDocumentModel).order_by(EnterpriseDocumentModel.created_at.desc()).limit(limit))).scalars();return [to_entity(x) for x in rows]
