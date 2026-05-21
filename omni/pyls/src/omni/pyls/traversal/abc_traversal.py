from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Generic, Self, TypeVar

T = TypeVar("T")


class TraversalStrategy(ABC, Generic[T], Iterator[T]):
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError
