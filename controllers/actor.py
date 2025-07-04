from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    try:
        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid data"), 400)
    return make_response(jsonify(new_actor), 200)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    # use this for 200 response code
    try:
        row_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)
    data.pop('id')  # видаляємо id з data, щоб не передавати його як атрибут
    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)
    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    row_id = int(data['id'])
    try:
        Actor.delete(row_id)
    except (KeyError, ValueError):
        return make_response(jsonify(error="There is no such an object to delete"), 400)
    # use this for 200 response code
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()

    try:
        actor_id = int(data['actor_id'])
        movie_id = int(data['movie_id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'actor_id' or 'movie_id'"), 400)

    actor_obj = Actor.query.get(actor_id)
    movie_obj = Movie.query.get(movie_id)

    if not actor_obj or not movie_obj:
        return make_response(jsonify(error="Actor or Movie not found"), 404)

    actor = Actor.add_relation(actor_id, movie_obj)

    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = [movie.name for movie in actor.filmography]  # зручно для читання
    return make_response(jsonify(rel_actor), 200)



def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    try:
        actor_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)

    actor_obj = Actor.query.get(actor_id)
    if not actor_obj:
        return make_response(jsonify(error="Actor not found"), 404)

    actor = Actor.clear_relations(actor_id)

    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = []  # після очищення – порожній список
    return make_response(jsonify(rel_actor), 200)
