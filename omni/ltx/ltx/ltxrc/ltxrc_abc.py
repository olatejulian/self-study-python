from abc import ABC, abstractmethod

from .__types__ import LtxrcDict


class LtxrcParser(ABC):
    @abstractmethod
    def get_configuration(self) -> LtxrcDict:
        raise NotImplementedError
