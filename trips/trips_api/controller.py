import pymongo
import json
from . import model

def create_trip(data, user_id):
    # Call the model function to create the trip in the database
    created_trip = model.create_trip_in_db(data, user_id)

    return created_trip

def get_accepted_trips(user_id):
    # Call the model function to get the trips from the database
    trips = model.get_trips_from_db(user_id)
    return trips