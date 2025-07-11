from flask import jsonify, make_response

from datetime import datetime
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data
from core import db


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

#
# def add_actor():
#     """
#     Add new actor
#     """
#     data = get_request_data()
#     ### YOUR CODE HERE ###
#
#     # use this for 200 response code
#     try:
#         new_record = Actor.create(**data)
#         new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
#     except (KeyError, ValueError):
#         return make_response(jsonify(error="Invalid data"), 400)
#     return make_response(jsonify(new_actor), 200)
#     ### END CODE HERE ###

DATE_FORMAT = "%d.%m.%Y"
REQUIRED_FIELDS = {"name", "gender", "date_of_birth"}
ALLOWED_FIELDS = REQUIRED_FIELDS  # актор не повинен мати інших полів

def add_actor():
    data = get_request_data()

    # 1. Перевірка, що всі потрібні поля присутні
    if not REQUIRED_FIELDS.issubset(data):
        return make_response(jsonify({"error": "Missing required fields"}), 400)

    # 2. Перевірка, що **немає зайвих полів**
    if not set(data).issubset(ALLOWED_FIELDS):
        return make_response(jsonify({"error": "Invalid fields present"}), 400)

    # 3. Перевірка формату дати
    try:
        datetime.strptime(data["date_of_birth"], DATE_FORMAT)
    except ValueError:
        return make_response(jsonify({"error": "Invalid date format. Use dd.mm.yyyy"}), 400)

    # 4. Створення запису
    try:
        new_record = Actor.create(**data)
    except AssertionError as e:
        return make_response(jsonify({"error": str(e)}), 500)

    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()

    try:
        row_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)

    data.pop('id')

    # Перевіримо, чи існує запис з таким id
    if not db.session.query(Actor).filter_by(id=row_id).first():
        return make_response(jsonify(error="Actor not found"), 400)

    # Перевіримо, що передані лише валідні поля
    for key in data:
        if key not in ACTOR_FIELDS:
            return make_response(jsonify(error=f"Invalid field '{key}'"), 400)

    # Перевіримо формат дати
    if 'date_of_birth' in data:
        try:
            datetime.strptime(data['date_of_birth'], "%d.%m.%Y")
        except ValueError:
            return make_response(jsonify(error="Invalid date format, expected dd.mm.yyyy"), 400)

    try:
        # Використовуємо твій метод update
        upd_record = Actor.update(row_id, **data)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return make_response(jsonify(error="Server error: " + str(e)), 500)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    try:
        row_id = int(data['id'])
    except (KeyError, ValueError):
        return make_response(jsonify(error="Invalid or missing 'id'"), 400)
    if not db.session.query(Actor).filter_by(id=row_id).first():
        return make_response(jsonify(error="Such actor shold exist "), 400)
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
    ### YOUR CODE HERE ###
    if 'id' and 'relation_id' in data.keys():
        try:
            actor_id = int(data['id'])
            movie_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        movie_data = Movie.query.filter_by(id=movie_id).first()
    except:
        err = 'Movie ID error'
        return make_response(jsonify(error=err), 400)

    try:
        actor = Actor.add_relation(actor_id, movie_data)  # add relation here
    except:
        err = 'Actor ID error'
        return make_response(jsonify(error=err), 400)

    # use this for 200 response code
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)

    ### END CODE HERE ###



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
        return make_response(jsonify(error="Actor not found"), 400)

    actor = Actor.clear_relations(actor_id)

    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = []  # після очищення – порожній список
    return make_response(jsonify(rel_actor), 200)
