from datetime import timedelta, datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime
from domain.models.base import Base
from typing import Union

class Roles:
    ROLE_ADMIN = "admin"
    ROLE_USER = "user"
    ROLE_SERVICES = "service"

class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),
                                     primary_key=True,
                                     default=uuid4)
    expiration_time: Mapped[Union[datetime, None]] = mapped_column(DateTime(timezone=True),
                                            nullable=True)


    def __init__(self, expiration: Union[int, None]):
        if expiration is not None:
            self.expiration_time = datetime.now() + timedelta(hours=expiration)
        else:
            self.expiration_time = None 
    
    def get_id(self) -> UUID:
        return self.id

    def get_expiration(self) -> Union[datetime, None]:
        return self.expiration_time
