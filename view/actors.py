from database.models import Actor, Movie, Gender
from flask import Blueprint, abort, jsonify

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
