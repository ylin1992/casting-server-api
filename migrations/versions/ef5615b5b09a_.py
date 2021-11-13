"""empty message

Revision ID: ef5615b5b09a
Revises: ac59f79ea006
Create Date: 2021-11-12 19:07:11.048383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef5615b5b09a'
down_revision = 'ac59f79ea006'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('actors_movies', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('actors_movies', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('actors_movies_movie_id_fkey', 'actors_movies', type_='foreignkey')
    op.drop_constraint('actors_movies_actor_id_fkey', 'actors_movies', type_='foreignkey')
    op.create_foreign_key(None, 'actors_movies', 'Actor', ['actor_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'actors_movies', 'Movie', ['movie_id'], ['id'], ondelete='cascade')
    op.alter_column('gender_actors', 'gender_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('gender_actors', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('gender_actors_gender_id_fkey', 'gender_actors', type_='foreignkey')
    op.drop_constraint('gender_actors_actor_id_fkey', 'gender_actors', type_='foreignkey')
    op.create_foreign_key(None, 'gender_actors', 'Gender', ['gender_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'gender_actors', 'Actor', ['actor_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'gender_actors', type_='foreignkey')
    op.drop_constraint(None, 'gender_actors', type_='foreignkey')
    op.create_foreign_key('gender_actors_actor_id_fkey', 'gender_actors', 'Actor', ['actor_id'], ['id'])
    op.create_foreign_key('gender_actors_gender_id_fkey', 'gender_actors', 'Gender', ['gender_id'], ['id'])
    op.alter_column('gender_actors', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('gender_actors', 'gender_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'actors_movies', type_='foreignkey')
    op.drop_constraint(None, 'actors_movies', type_='foreignkey')
    op.create_foreign_key('actors_movies_actor_id_fkey', 'actors_movies', 'Actor', ['actor_id'], ['id'])
    op.create_foreign_key('actors_movies_movie_id_fkey', 'actors_movies', 'Movie', ['movie_id'], ['id'])
    op.alter_column('actors_movies', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('actors_movies', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###