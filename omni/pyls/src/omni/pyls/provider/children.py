from collections.abc import Iterable, Iterator
from pathlib import Path

from omni.pyls.src.omni.pyls.filtering.abc_filtering import FilterStrategy
from omni.pyls.src.omni.pyls.sorting.abc_sorting import SortStrategy


class ChildrenCallbackProvider:
    def __init__(self, filterer: FilterStrategy, sorter: SortStrategy):
        self.__filterer = filterer
        self.__sorter = sorter

    def __call__(self, path: Path) -> Iterable[Path]:
        return self.__iter_children(path)

    def __iter_children(self, path: Path) -> Iterator[Path]:
        entries = path.iterdir()

        filtered_entries = (entry for entry in entries if self.__filterer.apply(entry))

        sorted_entries = sorted(filtered_entries, key=self.__sorter.key)

        for entry in sorted_entries:
            yield entry
