#!/usr/bin/python3
"""
This module list all the states in the database
"""
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """This method load cities in a state from the storage"""
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template("100-hbnb.html",
                           states=states,
                           amenities=amenities,
                           places=places)


@app.teardown_appcontext
def close_session(execute):
    """This method close the SQLAlchemy session"""
    return storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)