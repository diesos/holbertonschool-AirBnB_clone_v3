#!/usr/bin/python3
""" Index for API routes v1 """

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ stats of API"""
    object_count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(object_count)
