"""update_session_table

Revision ID: 54faf0049708
Revises: c795bc2c3c86
Create Date: 2024-11-24 22:06:02.324428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54faf0049708'
down_revision: Union[str, None] = 'c795bc2c3c86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('sessions', sa.Column('subject_id', sa.String(), nullable=False))
    op.add_column('sessions', sa.Column('topic_name', sa.String(), nullable=False))
    op.add_column('sessions', sa.Column('correct_answer_count', sa.Integer(), nullable=False, default=0))
    op.add_column('sessions', sa.Column('incorrect_answer_count', sa.Integer(), nullable=False, default=0))
    op.add_column('sessions', sa.Column('total_questions', sa.Integer(), nullable=False, default=0))
    op.add_column('sessions', sa.Column('total_time_spent', sa.String(), nullable=False))
    op.add_column('sessions', sa.Column('easy_question_count', sa.Integer(), nullable=False, default=0))
    op.add_column('sessions', sa.Column('medium_question_count', sa.Integer(), nullable=False, default=0))
    op.add_column('sessions', sa.Column('hard_question_count', sa.Integer(), nullable=False, default=0))

    op.drop_column('sessions', 'score')
    op.drop_column('sessions', 'time')
    op.drop_column('sessions', 'easy')
    op.drop_column('sessions', 'medium')
    op.drop_column('sessions', 'hard')

    op.create_foreign_key('fk_sessions_topic', 'sessions', 'topics', ['topic_id'], ['id'])

def downgrade():
    op.drop_column('sessions', 'subject_id')
    op.drop_column('sessions', 'topic_name')
    op.drop_column('sessions', 'correct_answer_count')
    op.drop_column('sessions', 'incorrect_answer_count')
    op.drop_column('sessions', 'total_questions')
    op.drop_column('sessions', 'total_time_spent')
    op.drop_column('sessions', 'easy_question_count')
    op.drop_column('sessions', 'medium_question_count')
    op.drop_column('sessions', 'hard_question_count')

    op.add_column('sessions', sa.Column('score', sa.String(), nullable=False))
    op.add_column('sessions', sa.Column('time', sa.Interval(), nullable=False))
    op.add_column('sessions', sa.Column('easy', sa.Integer(), nullable=False))
    op.add_column('sessions', sa.Column('medium', sa.Integer(), nullable=False))
    op.add_column('sessions', sa.Column('hard', sa.Integer(), nullable=False))

    op.drop_constraint('fk_sessions_topic', 'sessions', type_='foreignkey')
