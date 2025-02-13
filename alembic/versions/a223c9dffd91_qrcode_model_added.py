"""Qrcode model added

Revision ID: a223c9dffd91
Revises: 01dc6efebc3c
Create Date: 2024-08-31 15:44:33.263239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a223c9dffd91'
down_revision: Union[str, None] = '01dc6efebc3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('qr_code_image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number'),
    sa.UniqueConstraint('qr_code_image')
    )
    op.create_index(op.f('ix_codes_id'), 'codes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_codes_id'), table_name='codes')
    op.drop_table('codes')
    # ### end Alembic commands ###
