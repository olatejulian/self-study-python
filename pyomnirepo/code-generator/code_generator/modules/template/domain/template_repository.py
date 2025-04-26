from abc import ABC, abstractmethod
from typing import Iterator

from .template import Template


class TemplateRepository(ABC):
    @abstractmethod
    def save(self, template: Template) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, name: str) -> Template:
        raise NotImplementedError

    @abstractmethod
    def delete(self, name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> Iterator[Template]:
        raise NotImplementedError
