import os
import pymongo

def connect_drones():
    # Get the database user and password from Docker secrets

    db_user = os.getenv('DB_USER')

    db_password = os.getenv('DB_PASSWORD')
    
    # Get the database host from the environment variables
    db_host = os.getenv('DB_HOST')
    
    # Get the database name from the environment variables
    db_name = os.getenv('DB_NAME')
    
    # Create a MongoClient that will connect to the MongoDB database
    client = pymongo.MongoClient(f"mongodb+srv://{db_user}:{db_password}@{db_host}/{db_name}?retryWrites=true&w=majority",
                                tlsAllowInvalidCertificates=True
                                )
    
    # Get the database from the client
    db = client[db_name]
    
    # Get the collection name from the environment variables
    collection_name = os.getenv('DB_COLLECTION')

    # Get the collection from the database
    collection_drones = db[collection_name]

    return collection_drones

def get_drones_from_db(lat, lon, distance):
    if lon and lat and distance not in [None, ""]:
        items = connect_drones().find({
            'location': {
                '$near': {
                    '$geometry': {
                        'type': "Point",
                        'coordinates': [lon, lat]
                    },
                    '$maxDistance': distance,
                }
            }
        }, projection={'_id': False}).limit(1)
    else:
        items = connect_drones().find({}, projection={'_id': False})

    items_clean = [
        {
            "drone_id": item["drone_id"],
            "location": item["location"],
        }
        for item in items if "drone_id" in item and "location" in item
    ]
    
    return items_clean

    