"""add_opened_column

Revision ID: 04814f43f85c
Revises: 95349edf56b3
Create Date: 2024-12-26 20:58:14.105699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04814f43f85c'
down_revision: Union[str, None] = '95349edf56b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('flashcards', sa.Column('opened', sa.Boolean(), nullable=True, server_default='true'))

def downgrade() -> None:
    op.drop_column('flashcards', 'opened')
