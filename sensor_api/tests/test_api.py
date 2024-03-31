import requests

sensor_a = {"id": 3,
            "address": "NYC"}

res = requests.get("http://192.168.1.117:8080/sensor_api/test")
print(res.status_code)
res = requests.post("http://192.168.1.117:8080/sensor_api/add_sensor", json=sensor_a)
print(res.status_code)
