from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def collect_new_events(self) -> list:
        raise NotImplementedError
