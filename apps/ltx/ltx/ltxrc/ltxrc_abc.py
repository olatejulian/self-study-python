from abc import ABC, abstractmethod

from .__types__ import LtxrcDict


class Ltxrc(ABC):
    @abstractmethod
    def load(self) -> LtxrcDict:
        raise NotImplementedError
