#!/usr/bin/python3
"""This script starts a Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' when accessing the root URL."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display 'HBNB' when accessing the /hbnb URL."""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Display 'C ' followed by the value of the text variable."""
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """Display 'Python ' followed by the value of the text variable."""
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
