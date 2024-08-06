from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID


E = TypeVar("E")


class AbstractAsyncRepository(Generic[E], ABC):
    @abstractmethod
    async def create(self, entity: E) -> E:
        raise NotImplementedError()

    @abstractmethod
    async def read(self, id: UUID) -> E:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, entity: E) -> E:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError()
