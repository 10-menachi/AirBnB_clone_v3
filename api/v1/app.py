#!/usr/bin/python3
"""Flask app"""

from flask import Flask
from models import storage
from api.v1.views.index import index

app = Flask(__name__)
app.register_blueprint(index)


@app.teardown_appcontext
def teardown(exception):
    """Close the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    from os import getenv

    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)),
            threaded=True)
