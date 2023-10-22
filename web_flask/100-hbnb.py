#!/usr/bin/python3
"""
Flask web application to display an HBNB-like page.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display an HBNB-like page with States, Cities, Amenities, and Places.
    """
    states = storage.all(State).values()
    cities = storage.all(City).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()

    return render_template('100-hbnb.html',
                           states=states,
                           cities=cities,
                           amenities=amenities,
                           places=places)


@app.teardown_appcontext
def close_session(exception):
    """
    Remove the current SQLAlchemy Session after each request.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
