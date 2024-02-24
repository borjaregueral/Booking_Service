# Booking_Service

![Cabifly Helicopter](https://ichef.bbci.co.uk/images/ic/1920x1080/p061drx0.jpg)

Source: https://www.bbc.com/news/
## Description

Booking_Service is a cloud-based application composed of two microservices. It provides a booking system for free-floating mobility services, initially simulated using drones. However, the system can be adapted to use a more sophisticated simulator for cars or other vehicles.

### Drones API

The Drones API provides real-time information about available vehicles. It responds to GET requests with details of the vehicle closest to the user's location. Vehicle IDs and locations are managed through a Kafka message broker and stored in a MongoDB database. The system prioritizes vehicles within a 1000m radius of the user, expanding in 1000m increments if no vehicles are found.

### Trips API

The Trips API allows users to make bookings. Each booking is stored in a 'trips' collection with an initial status of "waiting". The booking manager assigns the closest available drone to each booking, changing its status to "accepted" and making it unavailable for further bookings. To avoid an infinite loop during booking assignment, the database is connected to Kafka through a Kafka connector.

Both APIs can be integrated with a front-end interface for user-friendly request handling.

## Technologies and Deployment

Booking_Service is built with Docker, Kafka, and MongoDB. It's deployed on AWS ECS, with two load balancers (one for each API) and service replicas. An API Gateway ensures a unique URL for both the Drones and Trips APIs.

## Installation

To install Booking_Service, follow these steps:

1. Clone the repository: `git clone https://github.com/borjaregueral/Booking_Service.git`

For the `drones` service:

2. Navigate to the drones directory: `cd Booking_Service/drones`
3. Build and run the Docker containers: `docker-compose up --build`

For the `trips` service:

4. Navigate to the trips directory: `cd ../trips`
5. Build and run the Docker containers: `docker-compose up --build`

Please ensure Docker and Docker Compose are installed and running on your machine before following these steps.

## Usage

To use Booking_Service, follow these steps:

1. Setup MongoDB with two collections `drones` and `trips`.
2. Setup Kafka.
3. Clone the repository: `git clone https://github.com/borjaregueral/Booking_Service.git`
4. Navigate to the `drones` directory: `cd Booking_Service/drones`
5. Build and run the Docker containers for the `drones` service: `docker-compose up --build`
6. Build and run the Docker containers for the `trips` service: `docker-compose up --build`
7. Start the MongoDB Kafka Source Connector with the appropriate configuration to stream changes from the `drones` and `trips` collections into Kafka topics. Refer to the Kafka Connect documentation for more details.
8. Your services are now running and ready to use!

Please ensure Docker, Docker Compose, MongoDB, and Kafka are installed and running on your machine before following these steps.

## Contributing

Contributions to Booking_Service are welcome! To contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes
4. Push to the branch: `git push origin feature-branch-name`
5. Create a pull request

## License

The project `Booking_Service` is licensed under the MIT License.
