from flask import Flask
from ismart_api.routes.sensor_api import sensor_api
from ismart_api.routes.sensor_data_api import sensor_data_api


def init_app():
    app = Flask(__name__)
    app.register_blueprint(sensor_api)
    app.register_blueprint(sensor_data_api)
    return app
