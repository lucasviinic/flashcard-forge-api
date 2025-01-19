"""add_origin_column_to_flashcards

Revision ID: e3b4e412526c
Revises: dc353f6833c4
Create Date: 2025-01-19 18:44:40.284030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3b4e412526c'
down_revision: Union[str, None] = 'dc353f6833c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('flashcards', sa.Column('origin', sa.String(), nullable=False, server_default='user'))
    op.create_check_constraint(
        'check_origin_valid_values',
        'flashcards',
        "origin IN ('user', 'ai')"
    )


def downgrade():
    op.drop_constraint('check_origin_valid_values', 'flashcards', type_='check')
    op.drop_column('flashcards', 'origin')