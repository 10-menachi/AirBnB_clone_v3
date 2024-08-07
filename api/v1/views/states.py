#!/usr/bin/python3

from api import app
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app.route('/states', methods=['GET'])
def get_states():
    """Returns the list of all State objects"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app.route('/states', methods=['POST'])
def post_states():
    """Creates a State object"""
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app.route('/states/<state_id>', methods=['DELETE'])
def delete_states(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app.route('/states/<state_id>', methods=['PUT'])
def put_states(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
