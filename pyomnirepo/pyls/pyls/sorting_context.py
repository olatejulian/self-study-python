from abc import ABC, abstractmethod
from typing import Callable, Generic, Iterable

from ._types import TContent, TOutput
from .directory import Directory
from .sorting_strategy import SortingStrategy


class SortingContext(ABC, Generic[TOutput]):
    @abstractmethod
    def sort(
        self,
        items: Iterable[TContent],
    ) -> list[TContent]: ...


class DefaultSortingContext(SortingContext[TOutput]):
    def __init__(
        self,
        sort_by_strategy: SortingStrategy[TOutput],
        reverse: bool,
        dirs_first: bool,
    ):
        self.__sort_by_strategy = sort_by_strategy
        self.__reverse = reverse
        self.__dirs_first = dirs_first

    def sort(
        self,
        items: Iterable[TContent],
    ) -> list[TContent]:
        return sorted(
            items,
            key=self.__sorting_key(self.__dirs_first, self.__reverse),
            reverse=self.__reverse,
        )

    def __sorting_key(
        self, dirs_first: bool, reverse: bool
    ) -> Callable[[TContent], tuple[int, TOutput]]:
        def sorting_key(content: TContent) -> tuple[int, TOutput]:
            type_order = 0 if isinstance(content, Directory) else 1

            if not dirs_first:
                type_order = 1 - type_order

            if reverse:
                type_order = 1 - type_order

            return (type_order, self.__sort_by_strategy(content))

        return sorting_key
