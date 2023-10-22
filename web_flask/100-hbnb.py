#!/usr/bin/python3
"""
Flask web application to display an HBNB-like page.
"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
app = Flask(__name__)


@app.teardown_appcontext
def dispose(exception):
    '''
    Remove session
    '''
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    '''
    display filters
    '''
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    data = {
        'states': list(states.values()),
        'amenities': list(amenities.values()),
        'places': list(places.values())
    }
    return render_template('100-hbnb.html', **data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
