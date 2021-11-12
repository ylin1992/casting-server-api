"""empty message

Revision ID: 500ce37794e1
Revises: 2d284d9817df
Create Date: 2021-11-12 17:14:03.699361

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '500ce37794e1'
down_revision = '2d284d9817df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Gender',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('release_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['Gender.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gender_actors',
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['Actor.id'], ),
    sa.ForeignKeyConstraint(['gender_id'], ['Gender.id'], )
    )
    op.drop_table('gender')
    op.drop_table('actor')
    op.drop_table('movie')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('release_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='movie_pkey')
    )
    op.create_table('actor',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='actor_pkey')
    )
    op.create_table('gender',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='gender_pkey')
    )
    op.drop_table('gender_actors')
    op.drop_table('Actor')
    op.drop_table('Movie')
    op.drop_table('Gender')
    # ### end Alembic commands ###
