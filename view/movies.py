from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify, request, current_app
from auth.auth import requires_auth
movies_route = Blueprint('movies_route', __name__)
'''
@TODO: add authentication
@TODO: add endpoints for delete and insert movie.actors
'''
@movies_route.route('', methods=['GET'])
@requires_auth(permission='get:movies')
def get_movies(jwt):
    movies = Movie.query.all()
    if (movies is None):
        abort(404)
    return jsonify({
            'success': True,
            'movies': [m.format() for m in movies]
        })

@movies_route.route('/<int:movie_id>', methods=['GET'])
@requires_auth(permission='get:movies')
def get_movie_by_id(jwt, movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    return jsonify({
            'success': True,
            'movie': movie.format()
        })

@movies_route.route('/<int:movie_id>', methods=['DELETE'])
@requires_auth(permission='delete:movie')
def delete_movie_by_id(jwt, movie_id):
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
@requires_auth(permission='patch:movie')
def patch_movie(jwt, movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400)
    
    try:
        for k in data:
            if k not in ['title', 'release_date']:
                abort(400)
            else:
                setattr(movie, k, data[k])
        movie.update()
    except Exception as e:
        abort(400)
    
    return jsonify({
        'success': True,
        'movie': movie.format()
    })
@movies_route.route('/<int:movie_id>/actors')
@requires_auth(permission='get:movies')
def get_actors_by_movie_id(jwt, movie_id):
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
        abort(404)
    
    try:
        actors = [a.id for a in movie.actors]
    except Exception as e:
        print(e)
        abort(422)
    
    return jsonify({
        "success": True,
        "actors_id": actors
    })
    
@movies_route.route('', methods=['POST'])
@requires_auth(permission='post:movie')
def post_request_movie(jwt):
    data = request.get_json()
    if data is None:
        abort(400)
    current_app.logger.info('Receving POST request: ' , data)
    
    if 'title' not in data or 'release_date' not in data:
        abort(400)
    
    if type(data['title']) is not str or type(data['release_date']) is not str:
        abort(422)
    
    if len(data['title']) == 0 or len(data['release_date']) == 0:
        abort(400)
    
    try:
        movie = Movie(title=data['title'],
                      release_date=data['release_date'],
                      )
        movie.insert()
    except Exception as e:
        abort(422)
    return jsonify({
        'success': True,
        'create': movie.format()
    })
