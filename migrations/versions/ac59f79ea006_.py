"""empty message

Revision ID: ac59f79ea006
Revises: ef49074d0ef6
Create Date: 2021-11-12 18:08:06.813533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac59f79ea006'
down_revision = 'ef49074d0ef6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Actor', sa.Column('age', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Actor', 'age')
    # ### end Alembic commands ###
