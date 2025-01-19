"""add_subscription_fields_to_users

Revision ID: dc353f6833c4
Revises: 04814f43f85c
Create Date: 2025-01-12 21:11:07.325100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc353f6833c4'
down_revision: Union[str, None] = '04814f43f85c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('users', sa.Column('account_type', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('max_flashcards', sa.Integer(), nullable=False, server_default='50'))
    op.add_column('users', sa.Column('flashcards_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('users', sa.Column('last_payment_date', sa.TIMESTAMP(), nullable=True))
    op.add_column('users', sa.Column('subscription_expiry', sa.TIMESTAMP(), nullable=True))


def downgrade():
    op.drop_column('users', 'subscription_expiry')
    op.drop_column('users', 'last_payment_date')
    op.drop_column('users', 'flashcards_count')
    op.drop_column('users', 'max_flashcards')
    op.drop_column('users', 'account_type')
