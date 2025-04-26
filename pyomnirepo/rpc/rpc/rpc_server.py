from __future__ import annotations

from typing import Any, Callable

from .abstracts import (
    HandlerRegister,
    RpcClientSocket,
    RpcServerSerializer,
    RpcSocket,
)
from .implementation import (
    JsonRpcServerSerializer,
    _HandlerRegister,
    _RpcSocket,
)
from .types import Handler
from .value_objects import Host, Port, RpcResponse


class RpcServer(HandlerRegister, RpcSocket):
    def __init__(
        self,
        host: str,
        port: int,
        serializer: RpcServerSerializer | None = None,
    ):
        __host = Host(host)
        __port = Port(port)

        self.__serializer = serializer or JsonRpcServerSerializer()
        self.__register: HandlerRegister = _HandlerRegister()
        self.__socket: RpcSocket = _RpcSocket(__host, __port)

    def __handle(self, __socket: RpcClientSocket):
        while True:
            try:
                encoded_request = __socket.get()

            except Exception as e:
                print(e)

                break

            else:
                request = self.__serializer.decode(encoded_request)

                if handler := self.__register.get_handler(request.handler_id):
                    data = handler(*request.args, **request.kwargs)

                    response = RpcResponse(data=data)

                    encoded_response = self.__serializer.encode(response)

                    __socket.send(encoded_response)

        __socket.close()

    def register_handler(self, handler: Handler, name: str | None = None):
        self.__register.register_handler(handler, name)

    def unregister_handler(self, handler_id: str | type[Any]):
        self.__register.unregister_handler(handler_id)

    def register_many(
        self,
        handlers: list[Handler | tuple[str, Handler]] | dict[str, Handler],
    ) -> None:
        self.__register.register_many(handlers)

    def get_handler(self, handler_id: str | type[Any]) -> Handler:
        return self.__register.get_handler(handler_id)

    def add_handler(self, handler: Callable[[RpcClientSocket], None]):
        self.__socket.set_handler(handler)

    def run(self):
        self.__socket.set_handler(self.__handle)

        print(
            f"Running RPC server on {self.__socket.host}:{self.__socket.port}"
        )
        try:
            self.__socket.run()

        except Exception as e:
            print(e)

        finally:
            self.__socket.close()

            print("RPC server stopped")
