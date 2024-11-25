"""add_user_id_to_session_table

Revision ID: 95349edf56b3
Revises: 54faf0049708
Create Date: 2024-11-25 19:44:04.354499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95349edf56b3'
down_revision: Union[str, None] = '54faf0049708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('sessions', sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True))

def downgrade():
    op.drop_column('sessions', 'user_id')
