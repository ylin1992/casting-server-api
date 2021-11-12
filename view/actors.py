from operator import ge
from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify, request
from database import utils

actors_route = Blueprint('actors_route', __name__)

@actors_route.route('/', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    print(actors)
    if (actors is None) or (len(actors) == 0):
        abort(404)
    return jsonify([actor.format() for actor in actors])

@actors_route.route('/<int:actor_id>', methods=['GET'])
def get_actor_by_id(actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    return jsonify(actor.format())

@actors_route.route('/<int:actor_id>', methods=['DELETE'])
def delete_actor_by_id(actor_id):
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
        abort(404)
    try:
        actor.delete()
    except Exception as e:
        print(e)
        abort(500)
    return jsonify({
        'success': True,
        'delete': actor_id
    })

@actors_route.route('', methods=['POST'])
def post_request_actor():
    data = request.get_json()
    print('Receving POST request: ', data)
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
        print(e)
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
            if (k == 'gender'):
                setattr(actor, 'gender_id', utils.get_gender_from_string(data[k]).id)
            elif (k == 'movies'):
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
        print(e)
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
        print(e)
        abort(422)
    
    return jsonify({
        "success": True,
        "movies_id": movies
    })