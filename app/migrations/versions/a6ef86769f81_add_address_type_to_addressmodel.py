"""Add address_type to AddressModel

Revision ID: a6ef86769f81
Revises: 16b05397d5ba
Create Date: 2024-09-14 09:22:41.535646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6ef86769f81'
down_revision: Union[str, None] = '16b05397d5ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addresses', sa.Column('address_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('addresses', 'address_type')
    # ### end Alembic commands ###
