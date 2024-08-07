from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..types import Handler, Handlers


class HandlerRegister(ABC):
    @abstractmethod
    def __add__(self, other: HandlerRegister):
        raise NotImplementedError

    @property
    @abstractmethod
    def handlers(self) -> Handlers:
        raise NotImplementedError

    @abstractmethod
    def register_handler(
        self, handler: Handler, name: str | None = None
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister_handler(self, handler_id: str | type[Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_many(
        self,
        handlers: list[Handler | tuple[str, Handler]] | dict[str, Handler],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_handler(self, handler_id: str | type[Any]) -> Handler:
        raise NotImplementedError
