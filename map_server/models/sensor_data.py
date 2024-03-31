from typing import Union
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from datetime import datetime

class SensorData:
    id: UUID
    sensor_id: int
    voltage: Union[float, None] 
    rain: Union[float, None] 
    distance: Union[int, None] 
    time: DateTime

    def __init__(self, id: UUID, sensor_id: int, voltage: Union[float, None], rain: Union[float, None],
                 distance: Union[int, None], time: DateTime):
        self.id = id
        self.sensor_id = sensor_id
        self.voltage = voltage
        self.rain = rain
        self.distance = distance
        self.time = time

    def get_id(self):
        return self.id

    def get_sensor_id(self):
        return self.sensor_id

    def get_voltage(self):
        return self.voltage

    def get_rain(self):
        return self.rain

    def get_distance(self):
        return self.distance

    def get_time(self):
        return self.time

    def set_id(self, id: UUID):
        self.id = id
        return self.id

    def set_sensor_id(self, sensor_id: int):
        self.sensor_id = sensor_id
        return self.sensor_id

    def set_voltage(self, voltage: float):
        self.voltage = voltage
        return self.voltage

    def set_rain(self, rain: float):
        self.rain = rain
        return self.rain

    def set_distance(self, distance: int):
        self.distance = distance
        return self.distance

    def set_time(self, time: DateTime):
        self.time = time
        return self.time

    def get_datetime_obj(self):
        dt = datetime.strptime(self.time, "%a, %d %b %Y %H:%M:%S %Z")
        return dt

    def get_date(self):
        dt = self.get_datetime_obj()
        d = dt.date()
        return d
