from typing import List
from interface import implements
from sqlalchemy import select, update, delete, func

from ...utils.app_types import Id
from ...utils.pagination import Pagination
from ...schemas.user_schema import UserCreate, UserUpdate, User

from ..models.user_sqlalchemy_model import UserModel
from ..interfaces.users_interface import IUserRepository
from ..implementations.sessions.sqlalchemy_session import SQLAlchemySession

class UserRepository(implements(IUserRepository)):
    def __init__(self, session = SQLAlchemySession()):
        self.session = session()

    def create(self, user: UserCreate) -> Id:
        with self.session.begin():
            new_user = UserModel(**user._fields())

            self.session.add(new_user)

            self.session.flush()

            return new_user.id

    def read(self, id: int) -> User:
        with self.session.begin():
            read_user = self.session.scalar(
                select(UserModel).where(UserModel.id == id)
            )

            user = User(**read_user._fields())

            return user

    def update(self, id: int, user_update: UserUpdate) -> None:
        with self.session.begin():
            self.session.execute(update(UserModel).where(UserModel.id == id).values(**user_update._fields()))

    def delete(self, id: int) -> None:
        with self.session.begin():
            self.session.execute(delete(UserModel).where(UserModel.id == id))

    def read_many(self, pagination: Pagination) -> List[User]:
        with self.session.begin():
            return self.session.execute(
                select(UserModel) \
                    .limit(pagination.limit) \
                    .offset(pagination.skip) \
                    .order_by(UserModel.created_at)
            )

    def count(self) -> int:
        with self.session.begin():
            return self.session.scalar(func.count(UserModel))
