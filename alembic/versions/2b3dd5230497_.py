"""empty message

Revision ID: 2b3dd5230497
Revises: 
Create Date: 2024-02-27 20:42:54.427689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b3dd5230497'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('flashcards', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_flashcards_user_id', 'flashcards', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_flashcards_user_id', 'flashcards', type_='foreignkey')
    op.drop_column('flashcards', 'user_id')
