from abc import ABC, abstractmethod

from .value_objects import Directory


class DirectoryLoader(ABC):
    @classmethod
    @abstractmethod
    def load(cls, dir_path: str) -> Directory:
        raise NotImplementedError
