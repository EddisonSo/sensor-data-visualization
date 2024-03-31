from uuid import UUID
from flask import Blueprint, jsonify, request
from domain.repo_exceptions import * 
from domain.repositories.sensor_data_repository import SensorDataRepository
from domain.models.sensor_data import SensorData 
from domain.models.sensor import Sensor
from sqlalchemy.orm import Session
from ismart_api.engine import engine

sensor_data_api = Blueprint('sensor_data_api', __name__, url_prefix="/data_api")

@sensor_data_api.route("/add_data", methods = ["POST"])
def add_sensor_data():
    context = request.get_json()
    sensor_data = SensorData()

    if context.get("sensor_id") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'sensor_id' parameter given"
            })
    try:
        sensor_data.set_sensor_id(int(context["sensor_id"]))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'id' parameter not an integer or cannot be interpreted as an integer"
            })
    with Session(engine) as session:
        if session.get(Sensor, sensor_data.get_sensor_id()) == None:
            return jsonify({
                "status": "failure",
                "reason": f"sensor with sensor_id {sensor_data.get_sensor_id()} does not exist"
                })
            

    if context.get("voltage") is not None: 
        try:
            sensor_data.set_voltage(float(context["voltage"]))
        except ValueError:
            return jsonify({
                "status": "failure",
                "reason": "'voltage' parameter not a float or cannot be interpreted as a float"
                })

    if context.get("rain") is not None:
        try:
            sensor_data.set_rain(float(context["rain"]))
        except ValueError:
            return jsonify({
                "status": "failure",
                "reason": "'rain' parameter not a float or cannot be interpreted as a float"
                })

    if context.get("distance") is not None:
        try:
            sensor_data.set_distance(int(context["distance"]))
        except ValueError:
            return jsonify({
                "status": "failure",
                "reason": "'distance' parameter not an integer or cannot be interpreted as an integer"
                })

    with Session(engine) as session:
        sensor_data_repository = SensorDataRepository(session)
        
        try:
            sensor_data_repository._add_sensor_data(sensor_data)
        except DBUnkownException:
            return jsonify({
                    "status": "failure",
                    "reason": "unknown server issue"
                })

        return jsonify({
                "status": "success",
                "sensor id": sensor_data.id
            })


@sensor_data_api.route("/get_data", methods= ["GET"])
def get_sensor_data():
    sensor_data_id = request.args['id']
    if not sensor_data_id:
        return jsonify({
            "status": "failure",
            "reason": "no 'id' parameter given" 
            })

    try:
        sensor_data_id = UUID(sensor_data_id)
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'id' parameter not an UUID or cannot be interpreted as an UUID"
            })

    with Session(engine) as session:
        sensor_repository = SensorDataRepository(session)
        try:
            sensor_data = sensor_repository.get_sensor_data(sensor_data_id)
        except DataDoesNotExist:
            return jsonify({
                    "status": "failure",
                    "reason": f"sensor_data with id {sensor_data_id} not found"
                })

        return jsonify({
            "status": "success",
            "sensor_data": SensorData.to_JSON(sensor_data)
            })

@sensor_data_api.route("/delete_data", methods= ["DELETE"])
def delete_sensor_data():
    sensor_id = request.args['id']

    if not sensor_id:
        return jsonify({
            "status": "failure",
            "reason": "no id parameter given" 
            })

    try:
        sensor_data_id = UUID(sensor_id)
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "sensor id not an integer"
            })

    with Session(engine) as session:
        sensor_data_repository = SensorDataRepository(session)
        try:
            sensor_data_id = sensor_data_repository.delete_sensor_data(sensor_data_id)
        except DataDoesNotExist:
            return jsonify({
                "status": "failure",
                "reason": f"sensor data with id {sensor_data_id} not found"
                })

        return jsonify({
            "status": "success",
            "reason": f"sensor data with id '{sensor_data_id}' removed"
            })

@sensor_data_api.route("/get_recent_data", methods= ["GET"])
def get_recent_data():
    sensor_id = request.args['sensor_id']
    if not sensor_id:
        return jsonify({
            "status": "failure",
            "reason": "no 'sensor_id' parameter given" 
            })

    try:
        sensor_id = int(sensor_id)
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'sensor id' parameter not an int or cannot be interpreted as an int"
            })

    with Session(engine) as session:
        sensor_repository = SensorDataRepository(session)
        try:
            sensor_data = sensor_repository.get_recent_data(sensor_id)
        except DataDoesNotExist:
            return jsonify({
                    "status": "failure",
                    "reason": f"sensor with id {sensor_id} does not have available data"
                })

        return jsonify({
            "status": "success",
            "sensor_data": SensorData.to_JSON(sensor_data)
            })

@sensor_data_api.route("/get_sensor_datas", methods= ["GET"])
def get_sensor_datas():
    context = request.get_json()

    if context.get("sensor_id") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'sensor_id' parameter given"
            })
    if context.get("date") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'date' parameter given"
            })
    if context.get("number") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'number' parameter given"
            })

    try:
        sensor_id = int(context.get("sensor_id"))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'sensor_id' parameter not an int or cannot be interpreted as an int"
            })
    try:
        number = int(context.get("number"))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'number' parameter not an int or cannot be interpreted as an int"
            })

    with Session(engine) as session:
        sensor_data_repository = SensorDataRepository(session)

        try:
            sensor_datas = sensor_data_repository.get_data_by_date(sensor_id, context.get("date"), number)
        except DateWrongFormat:
            return jsonify({
                "status": "failure",
                "sensor_datas": "'date' parameter not in correct format (ISO-8601)"
                })

        sensor_datas = list(map(lambda a: SensorData.to_JSON(a), sensor_datas))


        return jsonify({
            "status": "success",
            "sensor_datas": sensor_datas 
            })

@sensor_data_api.route("/get_sensor_datas_since", methods=["GET"])
def get_sensor_datas_since():
    context = request.get_json()

    if context.get("sensor_id") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'sensor_id' parameter given"
            })
    if context.get("hours") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'hours' parameter given"
            })
    if context.get("number") is None:
        return jsonify({
                "status": "failure",
                "reason": "no 'number' parameter given"
            })

    try:
        sensor_id = int(context.get("sensor_id"))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'sensor_id' parameter not an int or cannot be interpreted as an int"
            })
    try:
        hours = int(context.get("hours"))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'hours' parameter not an int or cannot be interpreted as an int"
            })
    try:
        number = int(context.get("number"))
    except ValueError:
        return jsonify({
            "status": "failure",
            "reason": "'number' parameter not an int or cannot be interpreted as an int"
            })

    with Session(engine) as session:
        sensor_data_repository = SensorDataRepository(session)
        sensor_datas = sensor_data_repository.get_data_since(sensor_id, hours, number)
        sensor_datas = list(map(lambda a: SensorData.to_JSON(a), sensor_datas))


        return jsonify({
            "status": "success",
            "sensor_datas": sensor_datas 
            })

