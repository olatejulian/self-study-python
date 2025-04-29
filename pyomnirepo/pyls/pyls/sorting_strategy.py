from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic

from .sorting_types import TContent, TOutput


class SortingStrategy(ABC, Generic[TOutput]):
    @abstractmethod
    def __call__(self, content: TContent) -> TOutput: ...


class SortByName(SortingStrategy[str]):
    def __call__(self, content: TContent) -> str:
        return content.name.lower()


class SortByAccessDate(SortingStrategy[datetime]):
    def __call__(self, content: TContent) -> datetime:
        return content.access_date


class SortByCreationDate(SortingStrategy[datetime]):
    def __call__(self, content: TContent) -> datetime:
        return content.creation_date


class SortByModificationDate(SortingStrategy[datetime]):
    def __call__(self, content: TContent) -> datetime:
        return content.modification_date
