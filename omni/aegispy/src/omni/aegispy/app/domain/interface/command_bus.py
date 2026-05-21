# pylint: disable=invalid-name
from abc import ABC, abstractmethod
from typing import TypeVar

from ....shared.command import Command, CommandHandler

CommandType = TypeVar(
    "CommandType",
    bound=Command,
)

CommandHandlerResponseType = TypeVar(
    "CommandHandlerResponseType",
)


class CommandDoesNotHaveHandlerException(Exception):
    pass


class CommandBus[CommandType: Command, CommandHandlerResponseType](ABC):
    def __init__(self, handlers: dict[type[CommandType], CommandHandler]):
        self.handlers = handlers

    @abstractmethod
    async def dispatch(self, command: CommandType) -> CommandHandlerResponseType:
        raise NotImplementedError
