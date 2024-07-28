#!/usr/bin/python3
"""A script that starts a flask web application"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Return a given string"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Return a given string"""
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Return a given string"""
    return 'C {}'.format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """Return a given string"""
    return 'C {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def num(n):
    """display n is a number only if n is an integer"""
    if isinstance(n, int):
        return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def html(n):
    """display n is a number only if n is an integer"""
    if isinstance(n, int):
        return render_template("5-number.html", n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """display n is a number only if n is an integer"""
    if isinstance(n, int):
        return render_template("6-number_odd_or_even", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
