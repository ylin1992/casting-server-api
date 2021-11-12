from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify, request

movies_route = Blueprint('movies_route', __name__)

@movies_route.route('', methods=['GET'])
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
@movies_route.route('/<int:movie_id>', methods=['PATCH'])
def patch_movie(movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400)
    
    try:
        for k in data:
            if (k == 'actors'):
                for i in data[k]:
                    actor = Actor.query.filter_by(id=i).one_or_none()
                    if actor is None:
                        abort(404)
                    else:
                        movie.actors.append(actor)
            else:
                setattr(movie, k, data[k])
        movie.update()
    except Exception as e:
        print(e)
        abort(400)
    
    return jsonify({
        'success': True,
        'movie': movie.format()
    })
