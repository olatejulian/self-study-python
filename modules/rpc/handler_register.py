from __future__ import annotations

import re
from typing import Any

from .types import Handler, Handlers


class HandlerRegister:
    @staticmethod
    def __pascal_to_snake(string: str) -> str:
        string = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", string)

        return string.lower()

    @classmethod
    def __type_name(cls, type_: type[Any]):
        return cls.__pascal_to_snake(type_.__name__)

    def __init__(self):
        self.__handlers: Handlers = {}

    def __add__(self, other: HandlerRegister):
        self.__handlers.update(other.handlers)

        return self

    @property
    def handlers(self):
        return self.__handlers

    def register(self, handler: Handler, name: str | None = None):
        handler_type = type(handler)
        handler_name = name if name else self.__type_name(handler_type)
        handler_function = handler

        self.__handlers[handler_name] = {
            "name": handler_name,
            "handler": handler_function,
            "handler_type": handler_type,
        }

        print()

    def unregister_handler(self, handler_id: str | type[Any]):
        if isinstance(handler_id, type):
            handler_id = self.__type_name(handler_id)

        del self.__handlers[handler_id]

    def register_many(
        self,
        handlers: list[Handler | tuple[str, Handler]] | dict[str, Handler],
    ):
        if isinstance(handlers, dict):
            for name, handler in handlers.items():
                self.register(name=name, handler=handler)

        elif isinstance(handlers, list):
            for item in handlers:
                if isinstance(item, tuple):
                    name, handler = item

                    self.register(handler=handler, name=name)

                else:
                    handler = item

                    self.register(handler)

    def get_handler(self, handler_id: str | type[Any]):
        if isinstance(handler_id, type):
            handler_id = self.__type_name(handler_id)

        return self.__handlers[handler_id]["handler"]
