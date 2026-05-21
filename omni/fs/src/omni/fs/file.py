from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


class File[T](ABC):
    def __init__(self, path: Path):
        self._path = path

    @abstractmethod
    def read(self) -> T: ...

    @abstractmethod
    def write(self, data: T) -> None: ...
