from abc import ABC, abstractmethod
from typing import Any

from .types import CommandHandler, EventHandler, QueryHandler


class CommandBus(ABC):
    @abstractmethod
    def add_command(
        self, command_type: type[Any], handler: CommandHandler
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def dispatch(self, command: Any) -> None:
        raise NotImplementedError


class EventBus(ABC):
    @abstractmethod
    def add_event(
        self, event_type: type[Any], handlers: list[EventHandler]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def dispatch(self, event: Any) -> None:
        raise NotImplementedError


class QueryBus(ABC):
    @abstractmethod
    def add_query(self, query: type[Any], handler: QueryHandler) -> None:
        raise NotImplementedError

    @abstractmethod
    async def dispatch(self, query: Any) -> Any:
        raise NotImplementedError
