from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from domain.models.sensor_data import SensorData
from domain.models.base import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creation_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True),
                                                    server_default=func.now())
    address: Mapped[str] = mapped_column(String(128),
                                         nullable=True)
    sensor_data: Mapped[List["SensorData"]] = relationship(
                                                backref="sensor",
                                                cascade="all, delete-orphan")

    longitude: Mapped[float] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=True)

    def get_id(self) -> int:
        return self.id

    def get_creation_time(self) -> DateTime:
        return self.creation_time

    def get_address(self) -> str:
        return self.address

    def get_longitude(self) -> float:
        return self.longitude

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude_latitude(self) -> list[float]:
        return [self.longitude, self.latitude]

    def set_longitude(self, longitude: float) -> float:
        self.longitude = longitude 
        return self.longitude

    def set_latitude(self, latitude: float) -> float:
        self.latitude = latitude
        return self.latitude

    def set_id(self, id: int) -> int:
        self.id = id
        return self.id

    def set_creation_time(self, creation_time: DateTime) -> DateTime:
        self.creation_time = creation_time
        return self.creation_time

    def set_address(self, address: str) -> str:
        self.address = address
        return self.address

    @staticmethod
    def to_JSON(sensor):
        return {
                "id": sensor.id,
                "creation_time": sensor.creation_time,
                "address": sensor.address,
                "longitude": sensor.longitude,
                "latitude": sensor.latitude
            }

