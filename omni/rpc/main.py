from dataclasses import dataclass
from typing import Callable


@dataclass
class RpcRequest:
    handler_id: str
    data: dict


@dataclass
class RpcResponse:
    data: dict


class RpcServer:
    def __init__(self):
        self.__handlers: dict[str, Callable] = {}

    def register_handler(self, handler_id: str, handler: Callable):
        self.__handlers[handler_id] = handler

    async def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration

    async def asend(self, request: RpcRequest):
        handler = self.__handlers[request.handler_id]

        return await handler(request.data)
