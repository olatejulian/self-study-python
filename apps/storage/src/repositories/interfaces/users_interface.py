'''
Links:
------
https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/
'''
from typing import List
from interface import Interface

from src.utils.pagination import Pagination
from src.schemas.user_schema import UserCreate, UserUpdate, User

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

    def read_many(self, pagination: Pagination) -> List[User]:
        pass

    def count(self) -> int:
        pass