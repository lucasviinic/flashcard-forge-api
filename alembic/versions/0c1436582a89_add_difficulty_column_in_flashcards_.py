"""add_difficulty_column_in_flashcards_table

Revision ID: 0c1436582a89
Revises: ea261d5ec6ea
Create Date: 2024-04-09 17:52:45.867782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c1436582a89'
down_revision: Union[str, None] = 'ea261d5ec6ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('flashcards', sa.Column('difficulty', sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column('flashcards', 'difficulty')