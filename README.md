# The ISmart Web Visualization Tool is comprised of the following services:

## ISmart API Service
The ISmart API controls the business logic behind the persistence and CRUD operations of the data that is collected from the sensor network.

## Map Service
The map service allows endusers to visualize data collected from the sensor network.

## MQTT Client Service
The MQTT client service listens to published by the LoRaWAN network MQTT service and pushes new data the the API service.

## Architecture Diagram
![Architecture](misc/arch.pdf)

## Usage
The Dockerfile describes the modules above as well as submodules required for the operation of the moduels above. To deploy the services run:
```
docker compose up -d
```

## Network Requirements
 - 80/443 for HTTP(S) for Map Service
 - 1883 for MQTT (SSL support is currently being developed)
