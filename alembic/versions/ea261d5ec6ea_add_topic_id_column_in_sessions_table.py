"""add_topic_id_column_in_sessions_table

Revision ID: ea261d5ec6ea
Revises: 3c2320bf2710
Create Date: 2024-04-09 17:15:29.661743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea261d5ec6ea'
down_revision: Union[str, None] = '3c2320bf2710'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('sessions', sa.Column('topic_id', sa.Integer, nullable=False))
    op.create_foreign_key('fk_sessions_topic_id', 'sessions', 'topics', ['topic_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_sessions_topic_id', 'sessions', type_='foreignkey')
    op.drop_column('sessions', 'topic_id')
