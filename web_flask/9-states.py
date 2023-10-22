#!/usr/bin/python3
"""This script starts a Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """Display a list of states from the database."""
    states = storage.all(State).values()
    return render_template('9-states.html', state=None, states=states)


@app.route('/states/<state_id>', strict_slashes=False)
def state_cities(state_id):
    """Display a list of cities for a specific state from the database."""
    state = storage.get(State, state_id)
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
