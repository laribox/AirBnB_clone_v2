#!/usr/bin/python3
"""
hbnb web static web flask
"""
from models import storage
from flask import Flask, render_template
from models.state import State
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)

@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays the main HBnB filters HTML page."""
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()

    states = sorted(states, key=lambda x: x.name)
    amenities = sorted(amenities, key=lambda x: x.name)
    places = sorted(places, key=lambda x: x.name)

    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")

