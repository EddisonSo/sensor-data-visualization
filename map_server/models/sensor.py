from sqlalchemy import DateTime
from datetime import date, datetime

class Sensor:
    id: int
    address: str
    creation_time: DateTime
    longitude: float
    latitude: float

    def __init__(self, id: int, address: str, creation_time: DateTime, longitude: float, latitude: float):
        self.id = id
        self.address = address
        self.creation_time = creation_time
        self.longitude = longitude
        self.latitude = latitude

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def get_creation_time(self):
        return self.creation_time

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def set_id(self, id: int):
        self.id = id

    def set_address(self, address: str):
        self.address = address

    def set_creation_time(self, creation_time: DateTime):
        self.creation_time = creation_time

    def set_longitude(self, longitude: float):
        self.longitude = longitude
        return self.longitude

    def set_latitude(self, latitude: float):
        self.latitude = latitude
        return self.latitude

    def get_datetime_obj(self):
        dt = datetime.strptime(self.creation_time, "%a, %d %b %Y %H:%M:%S %Z")
        return dt

    def get_date(self):
        dt = self.get_datetime_obj()
        d = dt.date()
        return d
