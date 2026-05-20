from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    @abstractmethod
    def create(self):
        raise NotImplementedError
