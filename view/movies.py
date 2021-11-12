from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify

movies_route = Blueprint('movies_route', __name__)

@movies_route.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    print(movies)
    if (movies is None) or (len(movies) == 0):
        abort(404)
    return jsonify([m.format() for m in movies])

@movies_route.route('/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    return jsonify(movie.format())

@movies_route.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie_by_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    try:
        movie.delete()
    except Exception as e:
        print(e)
        abort(500)
    return jsonify({
        'success': True,
        'delete': movie_id
    })
