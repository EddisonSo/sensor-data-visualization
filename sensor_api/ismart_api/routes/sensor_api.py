from flask import Blueprint, jsonify, request
from domain.repo_exceptions import *
from domain.repositories.sensor_repository import SensorRepository
from domain.models.sensor import Sensor
from sqlalchemy.orm import Session
from ismart_api.engine import engine
from ismart_api import api_check

sensor_api = Blueprint('sensor_api', __name__, url_prefix="/sensor_api")

@sensor_api.route("/add_sensor", methods = ["POST"])
@api_check.api_required
def add_sensor():
    context = request.get_json()
    longitude = None
    latitude = None
    address = context.get("address")
    if context.get("longitude") is not None:
        try:
            longitude = float(context.get("longitude"))
        except ValueError:
            return jsonify({
                    "status": "failure",
                    "reason": "longitude has to be floatable"
                })

    if context.get("latitude") is not None:
        try:
            latitude = float(context.get("latitude"))
        except ValueError:
            return jsonify({
                    "status": "failure",
                    "reason": "latitude has to be floatable"
                })

    if context.get("sensor_id") is not None:
        try:
            sensor_id = int(context.get("sensor_id"))
        except ValueError:
            return jsonify({
                    "status": "failure",
                    "reason": "sensor_id has to be floatable"
                })
    else:
        sensor_id = None

    with Session(engine) as session:
        sensor_repository = SensorRepository(session)
        try:
            new_sensor = sensor_repository.add_sensor(sensor_id=sensor_id, address=address, longitude=longitude, latitude=latitude)
        except DBUnkownException:
            return jsonify({
                    "status": "failure",
                    "reason": "unknown server issue"
                })

        return jsonify({
                "status": "success",
                "sensor id": new_sensor.id
            })


@sensor_api.route("/get_sensor", methods= ["GET"])
def get_sensor():
    context = request.get_json()
    sensor_id = context.get("sensor_id")
    if not sensor_id:
        return jsonify({
            "status": "failure",
            "reason": "no 'id' parameter given" 
            })

    try:
        sensor_id = int(sensor_id)
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'id' parameter not an integer or cannot be interpreted as an integer"
            })

    with Session(engine) as session:
        sensor_repository = SensorRepository(session)
        try:
            sensor = sensor_repository.get_sensor(sensor_id)
        except SensorDoesNotExist:
            return jsonify({
                    "status": "failure",
                    "reason": f"sensor with id {sensor_id} not found"
                })

        return jsonify({
            "status": "success",
            "sensor": Sensor.to_JSON(sensor)
            })

@sensor_api.route("/delete_sensor", methods= ["DELETE"])
@api_check.api_required
def delete_sensor():
    context = request.get_json()
    sensor_id = context.get("sensor_id")

    if not sensor_id:
        return jsonify({
            "status": "failure",
            "reason": "no sensor_id parameter given" 
            })

    try:
        sensor_id = int(sensor_id)
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "sensor id not an integer"
            })

    with Session(engine) as session:
        sensor_repository = SensorRepository(session)
        try:
            sensor = sensor_repository.delete_sensor(sensor_id)
        except SensorDoesNotExist:
            return jsonify({
                "status": "failure",
                "reason": f"sensor with id {sensor_id} not found"
                })
        return jsonify({
            "status": "success",
            "reason": f"sensor with id '{sensor}' removed"
            })

@sensor_api.route("/get_sensors", methods= ["GET"])
def get_sensors():
    with Session(engine) as session:
        sensor_repository = SensorRepository(session)

        sensors = sensor_repository.get_sensors()
        sensors = list(map(lambda a: Sensor.to_JSON(a), sensors))


        return jsonify({
            "status": "success",
            "sensors": sensors 
            })

@sensor_api.route("/test", methods= ["GET"])
def test():
    return "success"
