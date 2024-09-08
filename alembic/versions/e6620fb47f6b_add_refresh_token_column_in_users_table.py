"""add_refresh_token_column_in_users_table

Revision ID: e6620fb47f6b
Revises: 26acf748a33f
Create Date: 2024-09-08 18:40:08.537125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6620fb47f6b'
down_revision: Union[str, None] = '26acf748a33f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('refresh_token', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'refresh_token')
