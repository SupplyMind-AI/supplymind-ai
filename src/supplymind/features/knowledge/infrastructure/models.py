from __future__ import annotations
from datetime import datetime
from uuid import UUID,uuid4
from sqlalchemy import DateTime,Index,Integer,String,func
from sqlalchemy.dialects.postgresql import JSONB,UUID as PGUUID
from sqlalchemy.orm import Mapped,mapped_column
from supplymind.shared.infrastructure.database.base import Base
class EnterpriseDocumentModel(Base):
 __tablename__='enterprise_documents'; __table_args__=(Index('ix_enterprise_documents_status','status'),Index('ix_enterprise_documents_created','created_at'))
 id:Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),primary_key=True,default=uuid4)
 source_name:Mapped[str]=mapped_column(String(128),nullable=False); filename:Mapped[str]=mapped_column(String(512),nullable=False); checksum:Mapped[str]=mapped_column(String(64),unique=True,nullable=False,index=True); namespace:Mapped[str]=mapped_column(String(128),nullable=False); status:Mapped[str]=mapped_column(String(32),nullable=False); chunk_count:Mapped[int]=mapped_column(Integer,nullable=False,default=0); document_metadata:Mapped[dict]=mapped_column('metadata',JSONB,nullable=False,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now()); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
