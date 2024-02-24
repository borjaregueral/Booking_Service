import pymongo
from . import model
   
def get_closest_drone(lat, lon, distance):
    # Convert the parameters to float
    lon = float(lon) if lon else None
    lat = float(lat) if lat else None
    distance = int(distance) if distance else None

    # Connnect to the database
    model.connect_drones()
    # Call the function in the model
    closest_drone = model.get_drones_from_db(lat, lon, distance)

    return closest_drone