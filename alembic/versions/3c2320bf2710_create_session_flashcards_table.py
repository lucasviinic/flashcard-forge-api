"""create_session_flashcards_table

Revision ID: 3c2320bf2710
Revises: c722c276ce28
Create Date: 2024-04-09 14:38:44.556425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c2320bf2710'
down_revision: Union[str, None] = 'c722c276ce28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('session_flashcards',
        sa.Column('id', sa.Integer(), nullable=False, comment="Unique identifier"),
        sa.Column('session_id', sa.Integer(), sa.ForeignKey('sessions.id'), nullable=False, comment="Reference to session record ID"),
        sa.Column('flashcard_id', sa.Integer(), sa.ForeignKey('flashcards.id'), nullable=False, comment="Reference to flashcard record ID"),
        sa.Column('response', sa.Boolean(), nullable=False, comment="Answer given (correct or not)"),
        sa.Column('difficulty', sa.Integer(), nullable=False, comment="Flashcard difficulty, which can be 0, 1 or 2"),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment="Record creation date"),
        sa.Column('updated_at', sa.DateTime(), nullable=True, comment="Record update date"),
        sa.Column('deleted_at', sa.DateTime(), nullable=True, comment="Record deletion date"),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('session_flashcard')
