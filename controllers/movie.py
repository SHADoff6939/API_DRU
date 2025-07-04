from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mv = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mv)
    return make_response(jsonify(movies), 200)

def get_movie_by_id():
    data = get_request_data()
    try:
        row_id = int(data['id'])
        obj = Movie.query.filter_by(id=row_id).first()
        if not obj:
            return make_response(jsonify(error='Movie not found'), 404)
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(movie), 200)
    except (KeyError, ValueError):
        return make_response(jsonify(error='Invalid or missing id'), 400)

def add_movie():
    data = get_request_data()
    try:
        new_record = Movie.create(**data)
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(new_movie), 200)
    except (KeyError, ValueError) as e:
        return make_response(jsonify(error=f"Invalid data: {str(e)}"), 400)

def update_movie():
    data = get_request_data()
    try:
        row_id = int(data['id'])
        data.pop('id')  # Видаляємо id з даних для оновлення
        upd_record = Movie.update(row_id, **data)
        if not upd_record:
            return make_response(jsonify(error='Movie not found'), 404)
        upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    except (KeyError, ValueError):
        return make_response(jsonify(error='Invalid or missing id'), 400)

def delete_movie():
    data = get_request_data()
    try:
        row_id = int(data['id'])
        if not Movie.query.get(row_id):
            return make_response(jsonify(error='Movie not found'), 404)
        Movie.delete(row_id)
        return make_response(jsonify(message='Movie successfully deleted'), 200)
    except (KeyError, ValueError):
        return make_response(jsonify(error='Invalid or missing id'), 400)


def movie_add_relation():
    data = get_request_data()
    try:
        movie_id = int(data['movie_id'])
        actor_id = int(data['actor_id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error='Invalid or missing movie_id/actor_id'), 400)

    movie_obj = Movie.query.get(movie_id)
    actor_obj = Actor.query.get(actor_id)

    if not movie_obj or not actor_obj:
        return make_response(jsonify(error='Movie or Actor not found'), 404)

    movie = Movie.add_relation(movie_id, actor_obj)
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = [actor.name for actor in movie.cast]
    return make_response(jsonify(rel_movie), 200)

def movie_clear_relations():
    data = get_request_data()
    try:
        movie_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error='Invalid or missing id'), 400)

    movie_obj = Movie.query.get(movie_id)
    if not movie_obj:
        return make_response(jsonify(error='Movie not found'), 404)

    movie = Movie.clear_relations(movie_id)
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = []
    return make_response(jsonify(rel_movie), 200)