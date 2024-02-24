from flask import Flask, jsonify
import os
import time
import numpy as np
import json
from uuid import uuid4
from datetime import datetime
from kafka import KafkaProducer

geo_madrid = tuple(map(float, os.getenv('GEO_MADRID', '40.4168,-3.7038').split(',')))

NUM_DRONES = int(os.getenv('NUM_DRONES', '50'))
DISPERSION = float(os.getenv('DISPERSION', '0.01'))
MOVEMENT = float(os.getenv('MOVEMENT', '0.001'))

BOOTSTRAP_SERVERS = os.getenv('BOOTSTRAP_SERVERS', '52.86.37.2:9092')
topic = os.getenv('TOPIC', 'cabifly.drones')

producer = KafkaProducer(
    bootstrap_servers=[BOOTSTRAP_SERVERS],
    )

def create_random_drone(center, dispersion):
    return {
        "drone_id": str(uuid4()),
        "location": {
             'type': 'Point',
             'coordinates': [
                 center[1] + np.random.normal(0, dispersion), 
                 center[0] + np.random.normal(0, dispersion)
             ]
        }
    }

def update_drone(drone):
    if np.random.uniform() > 0.5:
        location = {
             'type': 'Point',
             'coordinates': [
                 drone["location"]["coordinates"][0] + np.random.normal(0, MOVEMENT), 
                 drone["location"]["coordinates"][1] + np.random.normal(0, MOVEMENT), 
             ]
        }
    else:
        location = drone["location"]
        
    return {
        "drone_id": drone["drone_id"],
        "location": location
    }

def simulate():
    drones = [create_random_drone(geo_madrid, DISPERSION) for _ in range(NUM_DRONES)]
    while True:  # simulate indefinitely
        drones = [update_drone(d) for d in drones]
        for d in drones:
            message = {
                "event": "drone_update",
                "timestamp": datetime.utcnow().isoformat(),
                "data": d
            }

            key = d["drone_id"].encode()
            value = json.dumps(message).encode()
            
            yield key, value 
        time.sleep(max(np.random.normal(2, 0.5), 0))


# Call the generator and send messages to Kafka
for key, value in simulate():
    producer.send(
        topic, 
        key=key, 
        value=value
    )

if __name__ == "__main__":
    # Call the generator and send messages to Kafka
    for key, value in simulate():
        producer.send(
            topic, 
            key=key, 
            value=value
        )