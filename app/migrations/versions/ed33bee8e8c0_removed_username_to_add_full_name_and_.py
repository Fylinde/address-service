"""Removed username to add full_name and phone

Revision ID: ed33bee8e8c0
Revises: a6ef86769f81
Create Date: 2024-09-23 08:42:27.018103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed33bee8e8c0'
down_revision: Union[str, None] = 'a6ef86769f81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('full_name', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('middle_name', sa.String(length=128), nullable=True))
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.drop_column('users', 'middle_name')
    op.drop_column('users', 'full_name')
    # ### end Alembic commands ###
