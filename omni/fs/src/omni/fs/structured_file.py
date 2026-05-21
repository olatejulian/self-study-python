from abc import ABC, abstractmethod
from typing import TypeVar

from .text_file import TextFile

T = TypeVar("T")


class StructuredFile[T](TextFile, ABC):
    @abstractmethod
    def load(self) -> T: ...

    @abstractmethod
    def dump(self, data: T) -> None: ...
