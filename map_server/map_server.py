from flask import Flask
from sensor_map import SensorMap

app = Flask(__name__)

@app.route("/")
def sensor_map():
    sensor_map = SensorMap()
    map_source = sensor_map.generate_map()
    if map_source is not None:
        return map_source
    return "Error", 500 

if __name__ == "__main__":
    app.run(host="0.0.0.0")
