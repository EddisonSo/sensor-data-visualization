from uuid import UUID
from domain.models.user import User
from sqlalchemy.orm import Session
from domain.repo_exceptions import *


class UserRepository():
    db_session: Session

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, expiration: int) -> User:
        if expiration == 0:
            new_user = User(expiration=None)
        else:
            new_user = User(expiration=expiration)
        self.db_session.add(new_user)
        self.db_session.commit()
        return new_user

    def get_user(self, uuid: UUID) -> User:
        user = self.db_session.get(User, uuid)
        if user is None:
            raise UserDoesNotExist()
        return user
