"""update_users_table_to_new_schema

Revision ID: 26acf748a33f
Revises: 0c1436582a89
Create Date: 2024-09-08 17:39:23.987845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26acf748a33f'
down_revision: Union[str, None] = '0c1436582a89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove colunas antigas
    op.drop_column('users', 'username')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'hashed_password')
    op.drop_column('users', 'profile_picture')

    # Adiciona novas colunas
    op.add_column('users', sa.Column('google_id', sa.String(), nullable=True, unique=True))
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('picture', sa.String(), nullable=True))


def downgrade() -> None:
    # Reverte para a estrutura anterior
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_picture', sa.String(), nullable=True))

    # Remove colunas novas
    op.drop_column('users', 'google_id')
    op.drop_column('users', 'name')
    op.drop_column('users', 'picture')