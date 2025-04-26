from abc import ABC, abstractmethod
from typing import Callable


class RpcClientSocket(ABC):
    @property
    @abstractmethod
    def client_address(self) -> tuple[str, int]:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def send(self, data: bytes) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class RpcSocket(ABC):
    @property
    @abstractmethod
    def host(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def port(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def set_handler(self, handler: Callable[[RpcClientSocket], None]) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
