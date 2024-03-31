from typing import Union
from uuid import UUID
from domain.models.sensor import Sensor
from domain.models.sensor_data import SensorData
from sqlalchemy.orm import Session
from domain.repo_exceptions import *
from datetime import datetime, timedelta
from sqlalchemy import cast, Date, desc
from sqlalchemy.orm import Query


class SensorDataRepository():
    db_session: Session

    def __init__(self, db_session: Session):
        self.session = db_session

    """
    Description: Add sensor data using SensorData object
    Arguments: new_data: SensorData representing sensor_data to be added
    Returns: sensor data: SensorData of added sensor data
    Throws: SensorDoesNotExist: sensor with sensor_id does not exist in sensor database
    """
    def _add_sensor_data(self, new_data: SensorData) -> SensorData:
        sensor_id = new_data.sensor_id
        if self.session.get(Sensor, sensor_id) == None:
            raise SensorDoesNotExist()
        self.session.add(new_data)
        self.session.commit()

        return new_data 

    """
    Description: Add sensor data
    Arguments: sensor_id: int sensor_id of sensor data, voltage: float (nullable) voltage reading, rain: float (nullable) rain level reading
               distance: int (nullable) distance reading
    Returns: sensor data: SensorData of added sensor data
    Throws: SensorDoesNotExist: sensor with sensor_id does not exist in sensor database
    """
    def add_sensor_data(self, sensor_id: int, voltage: Union[float, None], rain: Union[float, None], distance: Union[int, None]) -> SensorData:

        sensor_data = SensorData(sensor_id = sensor_id)
        if voltage:
            sensor_data.set_voltage(voltage)
        if rain:
            sensor_data.set_rain(rain)
        if distance:
            sensor_data.set_distance(distance)

        try:
            return self._add_sensor_data(sensor_data)
        except SensorDoesNotExist:
            raise SensorDoesNotExist()
    
    """
    Description: Modify sensor_data 
    Arguments: sensor_data_id: UUID of sensor_data to be modified, new_sensor: SensorData of new sensor data to be modified to
    Returns: sensor data: SensorData of modified sensor data 
    Throws: DataDoesNotExist: if no existing data with id sensor_data_id is found
            DataIDMismatch: if modified sensor data and to be modified sensor data does not have the same id
            SensorDoesNotExist: if modified sensor id does not exist in sensor database
    """
    def modify_sensor_data(self, sensor_data_id: UUID, new_sensor: SensorData) -> SensorData:
        sensor_data = self.session.get(SensorData, sensor_data_id)
        if not sensor_data:
            raise DataDoesNotExist()

        if sensor_data_id != sensor_data.get_id():
            raise DataIDMismatch()

        if self.session.get(Sensor, new_sensor.get_sensor_id()) == None:
            raise SensorDoesNotExist()

        sensor_data.set_rain(new_sensor.get_rain())
        sensor_data.set_voltage(new_sensor.get_voltage())
        sensor_data.set_distance(new_sensor.get_distance())
        sensor_data.set_sensor_id(new_sensor.get_sensor_id())

        self.session.commit()
        return new_sensor

    """
    Description: Retrieve sensor data by sensor_data_id 
    Arguments: sensor_data_id: UUID of sensor_data_id of sensor data to be retrieved
    Returns: Retrieved sensor_data: SensorData 
    Throws: DataDoesNotExist: if no data is found
    """
    def get_sensor_data(self, sensor_data_id: UUID) -> SensorData:
        sensor_data = self.session.get(SensorData, sensor_data_id)
        if not sensor_data:
            raise DataDoesNotExist()
        return sensor_data 

    """
    Description: Deletes sensor_data by sensor_data_id
    Arguments: sensor_data_id: UUID of sensor_data_id of sensor data to be deleted
    Returns: sensor_data_id: UUID of deleted sensor data
    Throws: DataDoesNotExist: if no data is found
    """
    def delete_sensor_data(self, sensor_data_id: UUID) -> UUID:
        sensor_data = self.session.get(SensorData, sensor_data_id)
        if not sensor_data:
            raise DataDoesNotExist()
        self.session.delete(sensor_data)
        self.session.commit()
        return sensor_data_id

    """
    Description: Retrieves most recent sensor data from sensor with sensor_id
    Arguments: sensor_id: integer of the sensor_id of datas to retreive 
    Returns: SensorData object
    Throws: DataDoesNotExist if no data is found
    """
    def get_recent_data(self, sensor_id: int) -> SensorData:
        sensor_data = self.session.query(SensorData).filter(SensorData.sensor_id == sensor_id).order_by(SensorData.time.desc()).first()
        if sensor_data is None:
            raise DataDoesNotExist()
        return sensor_data
    
    """
    Description: Retrieves all data obtained on a date. 
    Arguments: sensor_id: integer of the sensor_id of datas to retreive, date: str of datas to be retrieved in iso-8601 format i.e. "2023-07-20", limit: integer of maximum number of datas to retrieve, set 0 to retrieve all
    Returns: List of sensor datas
    Throws: None
    """
    def get_data_by_date(self, sensor_id: int, date: str, limit: int):
        try:
            datetime.fromisoformat(date)
        except:
            raise DateWrongFormat()

        if limit == 0:
            sensor_datas = self.session.query(SensorData).filter(SensorData.sensor_id == sensor_id).filter(cast(SensorData.time.op("AT TIME ZONE")("EST"), Date) == date).order_by(SensorData.time.desc()).all()
        else:
            sensor_datas = self.session.query(SensorData).filter(SensorData.sensor_id == sensor_id).filter(cast(SensorData.time.op("AT TIME ZONE")("EST"), Date) == date).order_by(SensorData.time.desc()).limit(limit)
        return sensor_datas 

    """
    Description: Retrieves sensor datas since hours_since hours ago
    Arguments: sensor_id: integer of the sensor_id of datas to retreive, hours_since: integer of number of hours ago worth of data to retrieve, limit: integer of maximum number of datas to retrieve, set 0 to retrieve all 
    Returns: List of sensor datas
    """
    def get_data_since(self, sensor_id: int, hours_since: int, limit: int):
        curr_time = datetime.utcnow()
        time_before = curr_time - timedelta(hours=hours_since)
        if limit == 0:
            data_since = self.session.query(SensorData).filter(SensorData.sensor_id == sensor_id).filter(SensorData.time > time_before).order_by(SensorData.time.desc()).all()
        else:
            data_since = self.session.query(SensorData).filter(SensorData.sensor_id == sensor_id).filter(SensorData.time > time_before).order_by(SensorData.time.desc()).limit(limit)
        return data_since

        

