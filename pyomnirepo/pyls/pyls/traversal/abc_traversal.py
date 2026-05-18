from abc import ABC, abstractmethod
from typing import Generic, Iterator, Self, TypeVar

T = TypeVar("T")


class TraversalStrategy(ABC, Generic[T], Iterator[T]):
    def __iter__(self) -> Self:
        return self

    @abstractmethod
    def __next__(self) -> T:
        raise NotImplementedError
