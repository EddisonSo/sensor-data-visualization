from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from domain import sensor_repository
from domain.sensor_repository import SensorRepository
from domain.base import Base
import unittest


engine = create_engine("postgresql://ismart:ismart@192.168.1.117:5432/ismart")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

class SensorDBUnitTest(unittest.TestCase):
    def test_add_sensors(self):
        with Session(engine) as session:
            sensor_repository = SensorRepository(session)
            sensor_1 = sensor_repository.add_sensor("Hoboken").get_id()
            sensor_2 = sensor_repository.add_sensor("Jersey City").get_id()
            sensor_3 = sensor_repository.add_sensor("").get_id()

        with Session(engine) as session:
            #test whether sensors have been created
            self.assertIsNotNone(sensor_repository.get_sensor(sensor_1))
            self.assertIsNotNone(sensor_repository.get_sensor(sensor_2))
            self.assertIsNotNone(sensor_repository.get_sensor(sensor_3))

            #test whether sensors have unique ids
            self.assertNotEqual(sensor_1, sensor_2)
            self.assertNotEqual(sensor_2, sensor_3)
            self.assertNotEqual(sensor_3, sensor_1)

    def test_delete_sensors(self):
        with Session(engine) as session:
            sensor_repository = SensorRepository(session)
            sensor_1 = sensor_repository.add_sensor("Hoboken")
            sensor_2 = sensor_repository.add_sensor("Jersey City")
            sensor_3 = sensor_repository.add_sensor("")





if __name__ == "__main__":
    unittest.main()
