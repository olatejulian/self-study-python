from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

KeyType = TypeVar("KeyType")


class SortStrategy[KeyType](ABC):
    @abstractmethod
    def key(self, path: Path) -> KeyType: ...
