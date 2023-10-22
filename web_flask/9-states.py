#!/usr/bin/python3
"""This script starts a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def dispose(exception):
    '''
    current session
    '''
    storage.close()


@app.route('/states/')
@app.route('/states/<id>', strict_slashes=False)
def states_with_id(id=None):
    '''
    list of state
    '''
    if id:
        id = 'State.{}'.format(id)
    return render_template('9-states.html', states=storage.all(State), id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
