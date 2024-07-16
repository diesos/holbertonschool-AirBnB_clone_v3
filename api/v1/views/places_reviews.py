#!/usr/bin/python3
""" Review API routes """

from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


# GET all Review (by place id)
# ============================================================================

@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrieves all reviews by place id """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = storage.all(Review).values()

    list_reviews = [review.to_dict()
                    for review in reviews if review.place_id == place_id]

    return jsonify(list_reviews)


# GET one review (id)
# ============================================================================

@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_one_review(review_id):
    """ Retrieves a review by its id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


# DELETE one review (id)
# ============================================================================

@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review by its id """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return jsonify({}), 200


# POST (create a review by place id)
# ============================================================================

@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """ Creates a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)

    if "text" not in data:
        abort(400, description="Missing text")

    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


# PUT (update a review by its id)
# ============================================================================

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def put_review(review_id):
    """ Updates a review by its id """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ["id",
                       "user_id",
                       "place_id",
                       "created_at",
                       "updated_at"
                       ]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
