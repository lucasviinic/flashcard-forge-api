"""create_session_table

Revision ID: c722c276ce28
Revises: 2b3dd5230497
Create Date: 2024-04-09 14:34:53.170613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c722c276ce28'
down_revision: Union[str, None] = '2b3dd5230497'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table('sessions',
        sa.Column('id', sa.Integer(), nullable=False, comment="Unique identifier"),
        sa.Column('score', sa.String(), nullable=False, comment="User score, e.g. 7/20"),
        sa.Column('time', sa.Interval(), nullable=False, comment="Study session duration 00:09:31"),
        sa.Column('easy', sa.Integer(), nullable=False, comment="Number of easy flashcards"),
        sa.Column('medium', sa.Integer(), nullable=False, comment="Number of medium flashcards"),
        sa.Column('hard', sa.Integer(), nullable=False, comment="Number of hard flashcards"),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment="Record creation date"),
        sa.Column('updated_at', sa.DateTime(), nullable=True, comment="Record update date"),
        sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Record deletion date"),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('sessions')
