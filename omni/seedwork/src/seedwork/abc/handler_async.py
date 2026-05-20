from abc import ABC, abstractmethod


class AbstractAsyncHandler(ABC):
    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def collect_new_events(self) -> list:
        raise NotImplementedError
