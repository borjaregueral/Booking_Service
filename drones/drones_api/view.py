import os
from flask import Blueprint, request, jsonify
from . import controller

# Create a blueprint
bp = Blueprint('drones_api', __name__, url_prefix='/')


@bp.get("/drones")
def get_drones():
    # Get the parameters from the request
    lon = request.args.get('lon')
    lat = request.args.get('lat')
    distance = request.args.get('distance')

    # Call the controller function and get the drones with the given parameters
    bookable_drone = controller.get_closest_drone(lon, lat, distance)

    # Return the result as a JSON response
    return jsonify(bookable_drone)

