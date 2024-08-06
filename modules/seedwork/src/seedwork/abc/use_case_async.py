from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractUseCase(Generic[T], ABC):
    @abstractmethod
    async def execute(self) -> T:
        raise NotImplementedError
