#!/usr/bin/python3
""" Script that starts a Flask web api """

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(self):
    """ Close the session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 error handler """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
