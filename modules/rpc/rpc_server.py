from __future__ import annotations

from .abstracts import RpcServerSerializer
from .handler_register import HandlerRegister
from .json_rpc_serializer import JsonRpcServerSerializer
from .rpc_socket import RpcClientSocket, RpcSocket
from .types import Handler
from .value_objects import Host, Port, RpcResponse


class RpcServer:
    def __init__(
        self,
        host: str,
        port: int,
        serializer: RpcServerSerializer | None = None,
    ):
        __host = Host(host)
        __port = Port(port)

        self.__serializer = serializer or JsonRpcServerSerializer()
        self.__register = HandlerRegister()
        self.__socket = RpcSocket(__host, __port)

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
        self.__register.register(handler, name)

    def run(self):
        print(
            f"Running RPC server on {self.__socket.host}:{self.__socket.port}"
        )
        try:
            self.__socket.run(self.__handle)

        except Exception as e:
            print(e)

        finally:
            self.__socket.close()

            print("RPC server stopped")
