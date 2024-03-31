from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from domain.models.base import Base


class SensorData(Base):
    __tablename__ = "sensor_data"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensors.id"),
                                           nullable=False)
    voltage: Mapped[float] = mapped_column(nullable=True)
    rain: Mapped[float] = mapped_column(nullable=True)
    distance: Mapped[int] = mapped_column(nullable=True)
    time: Mapped[DateTime] = mapped_column(DateTime(timezone=True),
                                           server_default=func.now())
    
    def get_id(self) -> UUID:
        return self.id

    def get_sensor_id(self) -> int:
        return self.sensor_id
    
    def get_voltage(self) -> float:
        return self.voltage

    def get_rain(self) -> float:
        return self.rain

    def get_distance(self) -> int:
        return self.distance

    def get_time(self) -> DateTime:
        return self.time

    def set_sensor_id(self, sensor_id: int) -> int:
        self.sensor_id = sensor_id
        return self.sensor_id

    def set_voltage(self, voltage: float) -> float:
        self.voltage = voltage
        return self.voltage

    def set_rain(self, rain: float) -> float:
        self.rain = rain
        return self.rain

    def set_distance(self, distance: int) -> int:
        self.distance = distance
        return self.distance

    @staticmethod
    def to_JSON(sensor_data):
        return {
                "id": sensor_data.id,
                "sensor_id": sensor_data.sensor_id,
                "voltage": sensor_data.voltage,
                "rain": sensor_data.rain,
                "distance": sensor_data.distance,
                "time": sensor_data.time,
                }

