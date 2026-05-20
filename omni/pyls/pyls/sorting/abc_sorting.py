from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

KeyType = TypeVar("KeyType")


class SortStrategy(ABC, Generic[KeyType]):
    @abstractmethod
    def key(self, path: Path) -> KeyType: ...
