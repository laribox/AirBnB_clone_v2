#!/usr/bin/python3
"""
display basic html for the hbnb project
"""

from flask import Flask, render_template
from models import *
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """display basic html for the hbnb project"""
    amenities = storage.all(Amenity).values()
    states = storage.all(State).values()
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
