import os
import json
import pymongo
import requests
from kafka import KafkaConsumer
from geopy.distance import geodesic
import time


def consume_trips():
    # Get the topic from the environment variables
    topic = os.getenv('TOPIC')
    
    # Get the bootstrap servers from the environment variables
    bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')

    # Get the auto_offset_reset value from the environment variables
    auto_offset_reset = os.getenv('AUTO_OFFSET_RESET')

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[bootstrap_servers],
        auto_offset_reset=auto_offset_reset
    )
    return consumer

def connect_trips():
    # Get the database user and password

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
    collection_trips = db[collection_name]

    return collection_trips


def process_trips():
    drones_api_url = os.getenv('DRONES_API_URL')
    for message in consume_trips():
        
        if message is None:
            print("No new bookings yet.")
            continue  # skip to the next iteration of the loop
        
        stream = json.loads(message.value.decode('utf-8'))
        payload = json.loads(stream['payload'])
        
        # Check if 'fullDocument' is in the payload
        if 'fullDocument' not in payload:
            continue
        # Access the fill document
        trip = payload['fullDocument']

        # If the status is waiting lookf for the closest drone
        if trip['status'] == 'waiting':
            lon, lat = trip['location']
            reference_point = (lon, lat)
            
            # Counter to increase distance in case no drone availabl within 1000 meters
            original_distance = 1000
            distance = original_distance
            closest_drone = None
            
            # while there is no donre in closest drone 
            while not closest_drone:
                params = {'lon': lon, 'lat': lat, 'distance': distance}
                response = requests.get(drones_api_url, params=params)
                closest_drone = response.json()
                
                # If there is no drone closeby look for more drones in 100m more
                if not closest_drone:
                    print(f"No drones available within {distance} meters. Increasing search radius...")
                    distance += 1000
                    increase_percentage = ((distance - original_distance) / original_distance) * 100
                    print(f"Search radius increased by {increase_percentage}%")
                    time.sleep(0.002)  # delay message for 2 milliseconds
                else:
                    # If there is assign the drone
                    connect_trips().update_one(
                        {'trip_id': trip['trip_id']},
                        {'$set': {'status': 'accepted', 'drone_id': closest_drone[0]['drone_id']}}
                    )

if __name__ == "__main__":
    process_trips()


