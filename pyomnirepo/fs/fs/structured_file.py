from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .text_file import TextFile

T = TypeVar("T")


class StructuredFile(TextFile, ABC, Generic[T]):
    @abstractmethod
    def load(self) -> T: ...

    @abstractmethod
    def dump(self, data: T) -> None: ...
