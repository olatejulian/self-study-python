from typing import List
from src.repositories.interfaces.users_interface import IUserRepository

class MockSession:
    def __init__(self):
        pass

class FakeUserRepository(IUserRepository):
    def __init__(self, mock_session: MockSession):
        pass

    def create(self, user) -> int:
        pass

    def read(self, id: int):
        pass

    def update(self, id: int, user_update) -> None:
        pass

    def delete(self, id: int) -> None:
        pass
