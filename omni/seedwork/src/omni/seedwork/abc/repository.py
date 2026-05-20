from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID


E = TypeVar("E")


class AbstractRepository(Generic[E], ABC):
    @abstractmethod
    def create(self, entity: E) -> E:
        raise NotImplementedError()

    @abstractmethod
    def read(self, id: UUID) -> E:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: E) -> E:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError()
