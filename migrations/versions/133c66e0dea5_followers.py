"""followers

Revision ID: 133c66e0dea5
Revises: 2b7aab863453
Create Date: 2018-12-03 09:17:45.438737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133c66e0dea5'
down_revision = '2b7aab863453'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
