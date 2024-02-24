import os
import pymongo
from datetime import datetime
from uuid import uuid4

def connect_trips():
    # Get the database user
    DB_USER = os.getenv('DB_USER')
        
    # Get the database password f
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # Get the database host from the environment variables
    db_host = os.getenv('DB_HOST')
    
    # Get the database name from the environment variables
    db_name = os.getenv('DB_NAME')
    
    # Create a MongoClient that will connect to the MongoDB database
    client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{db_host}/{db_name}?retryWrites=true&w=majority",
                                tlsAllowInvalidCertificates=True
                                )
    
    # Get the database from the client
    db = client[db_name]
    
    # Get the collection name from the environment variables
    collection_name = os.getenv('DB_COLLECTION')

    # Get the collection from the database
    collection_trips = db[collection_name]

    return collection_trips

def create_trip_in_db(data, user_id):
    # Prepare the document to be inserted
    trip = {
        'created_at': datetime.utcnow().isoformat(),
        'location': [data.get('lat'), data.get('lon')],
        'status': 'waiting',
        'trip_id': str(uuid4()),  # Generate a new UUID for each trip
        'user_id': user_id
    }

    # Insert the data into the collection
    result = connect_trips().insert_one(trip)

    # Add the _id of the inserted document to the trip dictionary
    trip['_id'] = str(result.inserted_id)
    
    # Remove the _id field from the trip dictionary
    trip.pop('_id', None)  

    return trip


def get_trips_from_db(user_id):
    trips = connect_trips().find({"user_id": user_id, "status": "accepted"})
    result = [
        {
            'trip_id': str(trip.pop('_id')),
            **trip
        } for trip in trips
    ]
    return result