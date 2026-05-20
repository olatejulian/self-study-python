from abc import ABC, abstractmethod
from typing import Any


class AbstractEntity(ABC):
    @abstractmethod
    def dict(self) -> dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def json(self) -> str:
        raise NotImplementedError()
