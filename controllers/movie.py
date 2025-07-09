from flask import jsonify, make_response
from datetime import datetime

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data
from core import db

REQUIRED_FIELDS = {"name", "genre", "year"}
ALLOWED_FIELDS = REQUIRED_FIELDS


def get_all_movies():
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mv = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mv)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    data = get_request_data()
    if 'id' not in data:
        return make_response(jsonify(error='No id specified'), 400)
    try:
        row_id = int(data['id'])
    except:
        return make_response(jsonify(error='Id must be integer'), 400)

    obj = Movie.query.filter_by(id=row_id).first()
    if not obj:
        return make_response(jsonify(error='Movie not found'), 400)

    movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(movie), 200)


def add_movie():
    data = get_request_data()

    # 1. check required fields
    if not REQUIRED_FIELDS.issubset(data):
        return make_response(jsonify(error='Missing required fields'), 400)

    # 2. check if there are any unexpected fields
    if not set(data).issubset(ALLOWED_FIELDS):
        return make_response(jsonify(error='Invalid fields present'), 400)

    # 3. check year is integer
    try:
        data['year'] = int(data['year'])
    except:
        return make_response(jsonify(error='Year must be an integer'), 400)

    try:
        new_record = Movie.create(**data)
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(new_movie), 200)
    except Exception as e:
        return make_response(jsonify(error='Invalid data'), 400)


def update_movie():
    data = get_request_data()
    try:
        row_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)

    data.pop('id')

    if not Movie.query.get(row_id):
        return make_response(jsonify(error="Movie not found"), 400)

    for key in data:
        if key not in ALLOWED_FIELDS:
            return make_response(jsonify(error=f"Invalid field '{key}'"), 400)

    if 'year' in data:
        try:
            data['year'] = int(data['year'])
        except ValueError:
            return make_response(jsonify(error="Year must be an integer"), 400)

    try:
        upd_record = Movie.update(row_id, **data)
        upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        return make_response(jsonify(upd_movie), 200)
    except Exception as e:
        return make_response(jsonify(error="Server error: " + str(e)), 500)


def delete_movie():
    data = get_request_data()
    try:
        row_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)

    if not Movie.query.get(row_id):
        return make_response(jsonify(error='Movie not found'), 400)

    try:
        Movie.delete(row_id)
        return make_response(jsonify(message='Movie successfully deleted'), 200)
    except Exception:
        return make_response(jsonify(error="Could not delete movie"), 500)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' and 'relation_id' in data.keys():
        try:
            row_id = int(data['id'])
            actor_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        actor_data = Actor.query.filter_by(id=actor_id).first()
    except:
        err = 'Actor ID error'
        return make_response(jsonify(error=err), 400)

    try:
        movie = Movie.add_relation(row_id, actor_data)
    except:
        err = 'Movie ID error'
        return make_response(jsonify(error=err), 400)

    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data:
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie = Movie.clear_relations(row_id)
    except:
        err = 'ID error'
        return make_response(jsonify(error=err), 400)

    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)
