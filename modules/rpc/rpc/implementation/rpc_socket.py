from __future__ import annotations

import socket
from multiprocessing import Process
from typing import Callable

from ..abstracts import RpcClientSocket, RpcSocket
from ..value_objects import Host, Port


class _RpcClientSocket(RpcClientSocket):
    def __init__(
        self,
        client_socket: socket.socket,
        client_address: tuple[str, int],
        buff_size: int = 1024,
    ):
        self.__client_socket = client_socket
        self.__client_address = client_address
        self.__buff_size = buff_size

    @property
    def client_address(self):
        return self.__client_address

    def get(self):
        return self.__client_socket.recv(self.__buff_size)

    def send(self, data: bytes):
        self.__client_socket.sendall(data)

    def close(self):
        self.__client_socket.close()


class _RpcSocket(RpcSocket):
    __socket: socket.socket
    __handler: Callable[[RpcClientSocket], None]

    def __init__(self, host: Host, port: Port, buff_size: int = 1024):
        self.__while = True
        self.__handlers_processes: list[Process] = []

        self.__host = host
        self.__port = port
        self.__buff_size = buff_size

        self.__init_socket()

    def __init_socket(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(self.__host), int(self.__port))

        self.__socket.bind(address)

        self.__socket.listen()

    @property
    def host(self):
        return str(self.__host)

    @property
    def port(self):
        return int(self.__port)

    def set_handler(self, handler: Callable[[RpcClientSocket], None]):
        self.__handler = handler

    def run(self):
        while self.__while:
            client_socket, client_address = self.__socket.accept()

            rpc_client_socket: RpcClientSocket = _RpcClientSocket(
                client_socket=client_socket,
                client_address=client_address,
                buff_size=self.__buff_size,
            )

            handlers_processes = Process(
                target=self.__handler,
                args=(rpc_client_socket,),
            )

            handlers_processes.start()

            self.__handlers_processes.append(handlers_processes)

    def close(self):
        for process in self.__handlers_processes:
            process.join()

            process.close()

        self.__socket.close()

        self.__while = False
