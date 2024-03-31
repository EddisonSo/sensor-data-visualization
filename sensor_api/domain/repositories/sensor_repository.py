from typing import Union
from domain.models.sensor import Sensor
from sqlalchemy.orm import Session
from domain.repo_exceptions import *


class SensorRepository():
    db_session: Session

    def __init__(self, db_session: Session):
        self.session = db_session

    def _add_sensor(self, new_sensor: Sensor) -> Sensor:
        self.session.add(new_sensor)
        self.session.commit()

        return new_sensor

    def add_sensor(self, sensor_id: Union[int, None], address: Union[str, None], longitude: Union[float, None], latitude: Union[float, None]) -> Sensor:
        new_sensor = Sensor()

        if address:
            new_sensor.set_address(address)
        
        if longitude:
            new_sensor.set_longitude(longitude)

        if latitude:
            new_sensor.set_latitude(latitude)

        if sensor_id:
            new_sensor.set_id(sensor_id)

        return self._add_sensor(new_sensor)
    
    def modify_sensor(self, sensor_id: int, new_sensor: Sensor) -> Sensor:
        sensor = self.session.get(Sensor, sensor_id)
        if not sensor:
            raise SensorDoesNotExist()

        if sensor_id != new_sensor.get_id():
            raise SensorIDMismatch()
        sensor.set_address(new_sensor.get_address())

        self.session.commit()
        return new_sensor

    def get_sensor(self, sensor_id: int) -> Sensor:
        sensor = self.session.get(Sensor, sensor_id)
        if not sensor:
            raise SensorDoesNotExist()
        return sensor

    def delete_sensor(self, sensor_id: int) -> int:
        sensor = self.session.get(Sensor, sensor_id)
        if not sensor:
            raise SensorDoesNotExist()
        self.session.delete(sensor)
        self.session.commit()
        return sensor_id 

    def get_sensors(self) -> list[Sensor]:
        sensors = self.session.query(Sensor).all()
        return sensors

