"""empty message

Revision ID: 92599035821d
Revises: 901b709d9695
Create Date: 2021-10-01 15:48:33.340038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92599035821d'
down_revision = '901b709d9695'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('group', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='group_pkey'),
    sa.UniqueConstraint('group', name='group_group_key')
    )
    # ### end Alembic commands ###
