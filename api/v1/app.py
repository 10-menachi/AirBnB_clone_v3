#!/usr/bin/python3
"""Flask app"""

from flask import Flask
from models import storage
from api.v1.views.index import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Close the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 status code response"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    from os import getenv

    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)),
            threaded=True)
