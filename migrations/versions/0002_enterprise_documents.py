"""Add enterprise document registry."""
from typing import Sequence,Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision='0002_enterprise_documents';down_revision='0001_phase3';branch_labels=None;depends_on=None
def upgrade():
 op.create_table('enterprise_documents',sa.Column('id',postgresql.UUID(as_uuid=True),primary_key=True),sa.Column('source_name',sa.String(128),nullable=False),sa.Column('filename',sa.String(512),nullable=False),sa.Column('checksum',sa.String(64),nullable=False),sa.Column('namespace',sa.String(128),nullable=False),sa.Column('status',sa.String(32),nullable=False),sa.Column('chunk_count',sa.Integer(),server_default='0',nullable=False),sa.Column('metadata',postgresql.JSONB(),server_default=sa.text("'{}'::jsonb"),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.Column('updated_at',sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False),sa.UniqueConstraint('checksum',name='uq_enterprise_documents_checksum'));op.create_index('ix_enterprise_documents_checksum','enterprise_documents',['checksum']);op.create_index('ix_enterprise_documents_status','enterprise_documents',['status'])
def downgrade(): op.drop_table('enterprise_documents')
