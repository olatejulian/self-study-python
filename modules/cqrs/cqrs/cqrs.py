import logging
from typing import Any

from .abstracts import CommandBus, EventBus, QueryBus
from .exceptions import (
    CannotExecuteHandlerException,
    UnregisteredCommandException,
    UnregisteredEventException,
    UnregisteredQueryException,
)
from .types import CommandHandler, EventHandler, QueryHandler


class ImplCommandBus(CommandBus):
    def __init__(self, logger: logging.Logger | None = None):
        self.__logger = logger or logging.getLogger()
        self.__commands: dict[type[Any], CommandHandler] = {}

    def add_command(
        self, command_type: type[Any], handler: CommandHandler
    ) -> None:
        self.__commands[command_type] = handler

    async def dispatch(self, command: Any) -> None:
        command_type = type(command)

        if handler := self.__commands[command_type]:
            try:
                await handler(command)

            except Exception as e:
                message = (
                    "CannotRunHandlerException\n"
                    + f"Event: {command_type}\n"
                    + f"Handler: {handler}\n"
                    + f"Exception: {e}"
                )

                self.__logger.exception(message)

        raise UnregisteredCommandException(command_type)


class ImplEventBus(EventBus):
    def __init__(self, logger: logging.Logger | None) -> None:
        self.__logger = logger or logging.getLogger()
        self.__events: dict[type[Any], list[EventHandler]] = {}

    def add_event(
        self, event_type: type[Any], handlers: list[EventHandler]
    ) -> None:
        if event_type in self.__events:
            self.__events[event_type].extend(handlers)

        self.__events[event_type] = handlers

    async def dispatch(self, event: Any) -> None:
        event_type = type(event)

        if handlers := self.__events[event_type]:
            for handler in handlers:
                try:
                    await handler(event)

                except Exception as e:
                    message = (
                        "CannotRunHandlerException\n"
                        + f"Event: {event_type}\n"
                        + f"Handler: {handler}\n"
                        + f"Exception: {e}"
                    )

                    self.__logger.exception(message)

        else:
            raise UnregisteredEventException(type(event))


class ImplQueryBus(QueryBus):
    def __init__(self):
        self.__queries: dict[type[Any], QueryHandler] = {}

    def add_query(self, query: type[Any], handler: QueryHandler) -> None:
        self.__queries[query] = handler

    async def dispatch(self, query: Any) -> Any:
        query_type = type(query)

        if query_type in self.__queries:
            handler = self.__queries[query_type]

            try:
                handler_return = await handler(query)

            except Exception as e:
                raise CannotExecuteHandlerException(e) from e

            else:
                return handler_return

        raise UnregisteredQueryException(query_type)
