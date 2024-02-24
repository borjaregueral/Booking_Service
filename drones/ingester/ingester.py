import os
import json
import pymongo
from kafka import KafkaConsumer


def consume_drones():
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

def connect_drones():
    # Get the database user and password from Docker secrets

    db_user = os.getenv('DB_USER')

    db_password = os.getenv('DB_PASSWORD')
    
    # Get the database host from the environment variables
    db_host = os.getenv('DB_HOST')
    
    # Get the database name from the environment variables
    db_name = os.getenv('DB_NAME')
    
    # Get the field name from the environment variables
    location_field = os.getenv('LOCATION_FIELD')   
    
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
    
    # Check if the collection already exists
    if collection_name not in db.list_collection_names():
        # If not, create it as a capped collection
        db.create_collection(
            collection_name,
            capped=True,
            max=50  # Maximum number of documents
        )
    
    # Create a 2dsphere index on the field
    collection_drones.create_index([(location_field, pymongo.GEOSPHERE)])

    return collection_drones


def process_message():
    connection = connect_drones()  
    consumer = consume_drones()
    # Consume the messages from Kafka
    for message in consumer:
        # The message value is a JSON object with the new drone position
        data_drones = json.loads(message.value.decode('utf-8'))
        drone_id = data_drones['data']['drone_id']
        location = data_drones['data']['location']


        # Print the data ingested from Kafka
        #print(f'Ingested data from Kafka: {data_drones}')

        # Prepare the document to insert/update
        doc = {
            'drone_id': drone_id,
            'location': location
        }
        # Update the drone data in MongoDB
        result = connection.update_one(
            {'drone_id': drone_id},  # Query: find the document with this drone_id
            {'$set': doc},  # Update: set the new data
            upsert=True  # If the document doesn't exist, create it
        ) 

        # Print the data posted to MongoDB
        #print(f'Posted data to MongoDB: {doc}')
        #print(f'Updated {result.modified_count} document(s)')
        

if __name__ == "__main__":
    process_message()