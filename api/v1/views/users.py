#!/usr/bin/python3
""" Users API routes """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.user import User


# GET all users
# ============================================================================

@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """ Retrieves all users """
    users = storage.all(User).values()

    list_users = [user.to_dict() for user in users]

    return jsonify(list_users)


# GET one user (id)
# ============================================================================

@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_one_user(user_id):
    """ Retrieves a user by its id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


# DELETE one user (id)
# ============================================================================

@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user by its id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({}), 200


# POST (create a user)
# ============================================================================

@app_views.route("/users", methods=["POST"], strict_slashes=False)
def post_user():
    """ Creates a user """
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


# PUT (update a user by its id)
# ============================================================================

@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def put_user(user_id):
    """ Updates a user by its id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict()), 200
