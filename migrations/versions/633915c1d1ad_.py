"""empty message

Revision ID: 633915c1d1ad
Revises: 34f57d366d51
Create Date: 2021-10-05 20:08:45.521550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '633915c1d1ad'
down_revision = '34f57d366d51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('first_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('_password', sa.String(length=200), nullable=True),
    sa.Column('photo', sa.String(length=20), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('learner', sa.Integer(), nullable=True),
    sa.Column('trainer', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['learner'], ['learner.id'], ),
    sa.ForeignKeyConstraint(['trainer'], ['trainer.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('user')
    op.drop_constraint('training_user_user_id_fkey', 'training_user', type_='foreignkey')
    op.create_foreign_key(None, 'training_user', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'training_user', type_='foreignkey')
    op.create_foreign_key('training_user_user_id_fkey', 'training_user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('_password', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('photo', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('learner', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('trainer', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name='user_group_id_fkey'),
    sa.ForeignKeyConstraint(['learner'], ['learner.id'], name='user_learner_fkey'),
    sa.ForeignKeyConstraint(['trainer'], ['trainer.id'], name='user_trainer_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('users')
    # ### end Alembic commands ###

import sqlalchemy_utils
