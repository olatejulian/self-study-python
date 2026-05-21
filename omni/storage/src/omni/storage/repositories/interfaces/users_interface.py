"""
Links:
------
https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/
"""

from interface import Interface

from omni.storage.src.omni.storage.schemas.user_schema import User, UserCreate, UserUpdate
from omni.storage.src.omni.storage.utils.pagination import Pagination


class IUserRepository(Interface):
    def __init__(self):
        pass

    def create(self, user: UserCreate) -> int:
        pass

    def read(self, id: int) -> User:
        pass

    def update(self, id: int, user_update: UserUpdate) -> None:
        pass

    def delete(self, id: int) -> None:
        pass

    def read_many(self, pagination: Pagination) -> list[User]:
        pass

    def count(self) -> int:
        pass
