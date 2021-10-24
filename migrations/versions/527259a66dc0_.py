"""empty message

Revision ID: 527259a66dc0
Revises: 051886d4dd55
Create Date: 2021-10-20 18:44:51.363455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '527259a66dc0'
down_revision = '051886d4dd55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('training', 'register')
    op.drop_column('training', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('training', sa.Column('status', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('training', sa.Column('register', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

import sqlalchemy_utils
