import requests
from models.sensor import Sensor
from models.sensor_data import SensorData

url = "192.168.1.117"
port = "8080"

def get_sensors():
    r = requests.get(f"http://{url}:{port}/sensor_api/get_sensors")
    if r.status_code != 200 or r.json().get("status") == "failure":
        return []

    sensors = r.json().get("sensors")
    result = []
    for sensor in sensors:
        result += [Sensor(
            id=sensor.get("id"),
            address=sensor.get("address"),
            creation_time=sensor.get("creation_time"),
            longitude=sensor.get("longitude"),
            latitude=sensor.get("latitude")
        )]
    return result

def get_recent(sensor_id: int):
    r = requests.get(f"http://{url}:{port}/data_api/get_recent_data?sensor_id={sensor_id}")
    if r.status_code != 200:
        return None

    if r.json().get("sensor_data") is None:
        return None

    sensor_data_json = r.json().get("sensor_data")

    sensor_data = SensorData(id=sensor_data_json.get("id"),
                             sensor_id=sensor_data_json.get("sensor_id"),
                             voltage=sensor_data_json.get("voltage"),
                             rain=sensor_data_json.get("rain"),
                             distance=sensor_data_json.get("distance"),
                             time=sensor_data_json.get("time"))
    return sensor_data

def get_sensor(sensor_id: int):
    r = requests.get(f"http://{url}:{port}/sensor_api/get_sensor?sensor_id={sensor_id}")
    if r.status_code != 200:
        return None

    if r.json().get("status") is None or r.json().get("status") == "failure":
        return None

    if r.json().get("sensor") is None:
        return None

    sensor_json = r.json().get("sensor_data")

    sensor_data = Sensor(id=sensor_json.get("id"),
                             address=sensor_json.get("address"),
                             creation_time=sensor_json.get("creation_time"),
                             longitude=sensor_json.get("longitude"),
                             latitude=sensor_json.get("latitude"))
    return sensor_data

def get_datas_by_sensor(sensor_id: int, date: str):
    request_json = {
        "sensor_id": sensor_id,
        "date": date,
        "number": 10000
        }
    r = requests.get(f"http://{url}:{port}/data_api/get_sensor_datas", json=request_json)
    if r.status_code != 200:
        return None

    if r.json().get("status") is None or r.json().get("status") == "failure":
        return None

    sensor_datas = r.json().get("sensor_datas")

    result = []
    for sensor in sensor_datas:
        result += [SensorData(
            id=sensor.get("id"),
            sensor_id=sensor.get("sensor_id"),
            voltage=sensor.get("voltage"),
            rain=sensor.get("rain"),
            distance=sensor.get("distance"),
            time=sensor.get("time")
        )]
    return result

def get_datas_since(sensor_id: int, hours: int):
    request_json = {
        "sensor_id": sensor_id,
        "hours": hours,
        "number": 10000
        }
    r = requests.get(f"http://{url}:{port}/data_api/get_sensor_datas_since", json=request_json)
    if r.status_code != 200:
        return None

    if r.json().get("status") is None or r.json().get("status") == "failure":
        return None

    sensor_datas = r.json().get("sensor_datas")

    result = []
    for sensor in sensor_datas:
        result += [SensorData(
            id=sensor.get("id"),
            sensor_id=sensor.get("sensor_id"),
            voltage=sensor.get("voltage"),
            rain=sensor.get("rain"),
            distance=sensor.get("distance"),
            time=sensor.get("time")
        )]
    return result
