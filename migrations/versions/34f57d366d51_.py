"""empty message

Revision ID: 34f57d366d51
Revises: fe22cbb526e6
Create Date: 2021-10-05 19:27:48.859489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34f57d366d51'
down_revision = 'fe22cbb526e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_name', sa.String(length=128), nullable=True))
    op.alter_column('user', 'photo',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.drop_column('user', 'lst_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('lst_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.alter_column('user', 'photo',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.drop_column('user', 'last_name')
    # ### end Alembic commands ###

import sqlalchemy_utils
