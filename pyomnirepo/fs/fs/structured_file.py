from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from .text_file import TextFile

T = TypeVar("T")
M = TypeVar("M", bound=BaseModel)


class StructuredFile(TextFile, ABC, Generic[T]):
    @abstractmethod
    def parse(self) -> T: ...

    @abstractmethod
    def dump(self, data: T) -> None: ...

    @abstractmethod
    def serialize(self, data: T) -> str: ...

    @abstractmethod
    def deserialize(self, data: str) -> T: ...

    @abstractmethod
    def validate(self, data: T, model: M) -> M: ...
