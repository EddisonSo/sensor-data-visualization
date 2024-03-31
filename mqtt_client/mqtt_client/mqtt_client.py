import paho.mqtt.subscribe as subscribe
import json
from . import config 
import requests
import logging
from math import isnan

class MqttClient():
    def __init__(self):
        subscribe.callback(self.get_message, topics=["#"], hostname=config.mqtt_address, port=1883)

    def test_get_message(self, client, userdata, message):
        print(message.payload)
        print(json.loads(message.payload.decode('utf-8')))

    def get_message(self, client, userdata, message):
        jsoned = json.loads(message.payload.decode('utf-8'))
        #payload = self.get_payload(jsoned)
        self.send_api(config.api_address, jsoned) 

    def get_payload(self, json_msg):
        if not (json_msg.get("uplink_message").get("decoded_payload") is None): 
            print(json_msg.get("uplink_message").get("decoded_payload"))
            return json_msg.get("uplink_message").get("decoded_payload")

    def send_api(self, api_address, message_payload):
        sensor_id = None
        voltage = None 
        rain = None
        distance = None

        if message_payload.get("sensor_id") is None:
            logging.error("sensor ID is None")
            return
        
        try:
            sensor_id = int(message_payload.get("sensor_id"))
        except ValueError:
            logging.error("invalid Sensor ID")

        if message_payload.get("voltage") is not None:
            try:
                voltage = float(message_payload.get("voltage"))
            except ValueError:
                logging.warning("voltage cannot be interpreted as a float or does not exist")
            if voltage is None or isnan(voltage):
                logging.warning("voltage does not exist")
                voltage = None

        if message_payload.get("rain_lvl") is not None:
            try:
                rain = float(message_payload.get("rain_lvl"))
            except ValueError:
                logging.warning("rain_lvl cannot be interpreted as a float or does not exist")
            if rain is None or isnan(rain):
                logging.warning("rain_lvl does not exist")
                rain = None
                
        if message_payload.get("distance") is not None:
            try:
                distance = int(message_payload.get("distance"))
            except ValueError:
                logging.warning("distance cannot be interpreted as an integer or does not exist")

        json = {
            "sensor_id": sensor_id,
            "voltage": voltage,
            "rain": rain,
            "distance": distance 
        }

        try:
            status = requests.post(api_address, json=json)
            if status.status_code >= 300:
                logging.warning("api request responded with a non 200 level response code")

            if status.json().get("status") != "success":
                logging.warning("api request responded with a failure")
            else:
                logging.info(f"successfully pushed new data for sensor with sensor_id {sensor_id}")

        except:
            logging.error("unable to connect to server api")


if __name__ == "__main__":
    client = MqttClient()
