"""initial_migration

Revision ID: c795bc2c3c86
Revises: 
Create Date: 2024-09-16 20:43:49.147988

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c795bc2c3c86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'users' table
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('google_id', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('picture', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    # Create the 'subjects' table
    op.create_table(
        'subjects',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('subject_name', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    # Create the 'topics' table
    op.create_table(
        'topics',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('subject_id', sa.UUID(as_uuid=True), sa.ForeignKey('subjects.id'), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('topic_name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    # Create the 'flashcards' table
    op.create_table(
        'flashcards',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('subject_id', sa.UUID(as_uuid=True), sa.ForeignKey('subjects.id'), nullable=True),
        sa.Column('topic_id', sa.UUID(as_uuid=True), sa.ForeignKey('topics.id'), nullable=True),
        sa.Column('question', sa.String(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.Column('last_response', sa.Boolean(), default=None),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    # Create the 'sessions' table
    op.create_table(
        'sessions',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('topic_id', sa.UUID(as_uuid=True), sa.ForeignKey('topics.id'), nullable=True),
        sa.Column('score', sa.String(), nullable=False),
        sa.Column('time', sa.Interval(), nullable=False),
        sa.Column('easy', sa.Integer(), nullable=False),
        sa.Column('medium', sa.Integer(), nullable=False),
        sa.Column('hard', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )

    # Create the 'session_flashcards' table
    op.create_table(
        'session_flashcards',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
        sa.Column('session_id', sa.UUID(as_uuid=True), sa.ForeignKey('sessions.id'), nullable=True),
        sa.Column('flashcard_id', sa.UUID(as_uuid=True), sa.ForeignKey('flashcards.id'), nullable=True),
        sa.Column('response', sa.Boolean(), nullable=False),
        sa.Column('difficulty', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now(), nullable=True),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    # Drop the 'session_flashcards' table
    op.drop_table('session_flashcards')

    # Drop the 'sessions' table
    op.drop_table('sessions')

    # Drop the 'flashcards' table
    op.drop_table('flashcards')

    # Drop the 'topics' table
    op.drop_table('topics')

    # Drop the 'subjects' table
    op.drop_table('subjects')

    # Drop the 'users' table
    op.drop_table('users')
