from operator import ge
from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify, request, current_app
from database import utils
from auth.auth import requires_auth

actors_route = Blueprint('actors_route', __name__)

@actors_route.route('', methods=['GET'])
@requires_auth(permission='get:actors')
def get_actors(jwt):
    actors = Actor.query.all()
    if (actors is None):
        abort(404)
    return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        })

@actors_route.route('/<int:actor_id>', methods=['GET'])
@requires_auth(permission='get:actors')
def get_actor_by_id(jwt, actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    return jsonify({
            'success': True,
            'actor': actor.format()
        })

@actors_route.route('/<int:actor_id>', methods=['DELETE'])
@requires_auth(permission='delete:actor')
def delete_actor_by_id(jwt, actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
    except Exception as e:
        current_app.logger.exception(e)
        abort(500)
    return jsonify({
        'success': True,
        'delete': actor_id
    })

@actors_route.route('', methods=['POST'])
@requires_auth(permission='post:actor')
def post_request_actor(jwt):
    data = request.get_json()
    current_app.logger.info('Receving POST request: ' , data)
    if 'name' not in data or 'age' not in data or 'gender' not in data:
        abort(400)
    gender = utils.get_gender_from_string(data['gender'])
    if gender is None:
        abort(400)
    try:
        actor = Actor(name=data['name'],
                      age=data['age'],
                      gender_id=gender.id)
        actor.insert()
    except Exception as e:
        current_app.logger.exception(e)
        abort(500)
    return jsonify({
        'success': True,
        'create': actor.format()
    })
    
@actors_route.route('/<int:actor_id>', methods=['PATCH'])
def patch_actor(actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    
    data = request.get_json()
    if data is None:
        abort(400)
    
    
    try:
        for k in data:
            if k not in ['gender', 'name', 'age', 'movies']:
                abort(400)
            elif (k == 'gender'):
                gender = utils.get_gender_from_string(data[k])
                if gender is None:
                    abort(400)
                gender_id = gender.id
                setattr(actor, 'gender_id', gender_id)
            elif (k == 'movies'):
                actor.movies = []
                for i in data[k]:
                    movie = Movie.query.filter_by(id=i).one_or_none()
                    if movie is None:
                        abort(404)
                    else:
                        actor.movies.append(movie)
            else:
                setattr(actor, k, data[k])
        actor.update()
    except Exception as e:
        current_app.logger.exception(e)
        abort(400)
    
    return jsonify({
        'success': True,
        'actor': actor.format()
    })

@actors_route.route('/<int:actor_id>/movies')
def get_movies_by_actor_id(actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    
    try:
        movies = [m.id for m in actor.movies]
    except Exception as e:
        current_app.logger.exception(e)
        abort(422)
    
    return jsonify({
        "success": True,
        "movies_id": movies
    })