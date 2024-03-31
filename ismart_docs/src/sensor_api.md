# Sensor API

The Sensor API allows other services and users to access the Sensor data via its many endpoints.

## Add Sensor (POST)
```
https://{api-service-url}/sensor_api/add_sensor
```
/sensor_api/add_sensor allows services and users to add a new sensor to the database to be persisted. It consumes the following fields pass as JSON for authorization and input parameters:
```JSON
{
    "api_key": "string, required for authorization",
    "address": "string, optional",
    "longitude": "float, optional",
    "latitude": "float, optional"
}
```
It returns the following JSON on success:
```JSON
{
    "status": "indicates successful operation"
    "sensor_id": "int, sensor_id of sensor that was added to the database"
}
```

## Get Sensor (GET)
```
https://{api-service-url}/sensor_api/get_sensor
```
/sensor_api/get_sensor allows services and users to add a get sensor metadata. It consumes the following fields pass as JSON for authorization and input parameters:
```JSON
{
    "api_key": "string, required for authorization",
    "sensor_id": "int, required"
}
```
It returns the following JSON on success:
```JSON
{
    "status": "indicates successful operation"
    "sensor_id": "int, sensor_id of sensor that was retrieved from database"
    "address": "string",
    "longitude": "float",
    "latitude": "float",
    "creation_date": "DateTime"
}
```

## Delete Sensor (DELETE)
```
https://{api-service-url}/sensor_api/delete_sensor
```
/sensor_api/delete_sensor allows services and users to delete an existing sensor. It consumes the following fields pass as JSON for authorization and input parameters:
```JSON
{
    "api_key": "string, required for authorization",
    "sensor_id": "int, required for sensor with sensor_id to be deleted"
}
```
It returns the following JSON on success:
```JSON
{
    "status": "indicates successful operation"
    "sensor_id": "int, sensor_id of sensor that was deleted from database"
}
```

## Get Sensors (GET)
```
https://{api-service-url}/sensor_api/get_sensors
```
/sensor_api/get_sensors allows services and users to add a get sensor metadata for all sensors. It consumes the following fields pass as JSON for authorization and input parameters:
```JSON
{
    "api_key": "string, required for authorization",
}
```
It returns the following JSON on success:
```JSON
{
    "status": "indicates successful operation"
    "sensors: "list of sensor objects"
    [
        "sensor_id": "int, sensor_id of sensor that was retrieved from database",
        "address": "string",
        "longitude": "float",
        "latitude": "float",
        "creation_date": "DateTime"
    ]
}
```
