from ..repositories.implementations.user_sqlalchemy_repository import UserRepository
from ..schemas.user_schema import User, UserCreate, UserUpdate
from ..utils.app_types import Id
from ..utils.pagination import Pagination


class UserService:
    def __init__(self, repository: UserRepository = UserRepository()):
        self.repository = repository

    def create(self, user: UserCreate) -> int:
        return self.repository.create(user)

    def read(self, id: Id) -> User:
        return self.repository.read(id)

    def update(self, id: Id, user: UserUpdate) -> None:
        self.repository.update(id, user)

    def delete(self, id: Id) -> None:
        self.repository.delete(id)

    def read_many(self, pagination: Pagination) -> list[User]:
        return self.repository.read_many(pagination)

    def count(self) -> int:
        return self.repository.count()
