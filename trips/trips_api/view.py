import os
from flask import Blueprint, request, jsonify
from . import controller

# Create a blueprint
bp = Blueprint('trips_api', __name__, url_prefix='/')

@bp.post("/users/<user_id>/trips")
def post_trips(user_id):
    # Parse the incoming JSON request
    data = request.get_json()

    # Call the controller function to create the trip
    trip = controller.create_trip(data, user_id)

    return jsonify(trip), 201


@bp.get("/users/<user_id>/trips")
def get_trips(user_id):
    # Call the controller function to get the trips
    trips = controller.get_accepted_trips(user_id)

    # Check if trips is empty
    if not trips:
        return jsonify({"Error": "That user didn't book with us"}), 404

    return jsonify(trips), 200
