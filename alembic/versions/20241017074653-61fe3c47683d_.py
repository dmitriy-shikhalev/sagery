"""empty message

Revision ID: 61fe3c47683d
Revises: 93145e3f94fb
Create Date: 2024-10-17 07:46:53.228723

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '61fe3c47683d'
down_revision: Union[str, None] = '93145e3f94fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'value', existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'value', existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
