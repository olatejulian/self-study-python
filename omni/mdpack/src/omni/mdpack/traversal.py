from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Protocol

from pathspec import PathSpec


class TraversalEventType(Enum):
    ENTER_DIRECTORY = auto()
    EXIT_DIRECTORY = auto()
    FILE = auto()


@dataclass(slots=True, frozen=True)
class TraversalEvent:
    type: TraversalEventType
    path: Path
    depth: int
    is_last: bool


class TraversalListener(Protocol):
    def consume(
        self,
        event: TraversalEvent,
    ) -> None: ...


class PathTraversal:
    """
    Event-driven depth-first traversal.
    """

    def __init__(
        self,
        root: Path,
        ignore_patterns: list[str] | None = None,
    ) -> None:
        self.__root = root.resolve()

        self.__spec = PathSpec.from_lines(
            "gitwildmatch",
            ignore_patterns or [],
        )

    def walk(
        self,
    ) -> Iterator[TraversalEvent]:
        yield from self.__walk_directory(
            self.__root,
            depth=0,
            is_last=True,
        )

    def __walk_directory(
        self,
        directory: Path,
        depth: int,
        is_last: bool,
    ) -> Iterator[TraversalEvent]:
        yield TraversalEvent(
            type=TraversalEventType.ENTER_DIRECTORY,
            path=directory,
            depth=depth,
            is_last=is_last,
        )

        children = [
            child
            for child in sorted(
                directory.iterdir(),
                key=self.__sort_key,
            )
            if not self.__is_ignored(child)
        ]

        for index, child in enumerate(children):
            child_is_last = index == len(children) - 1

            if child.is_dir():
                yield from self.__walk_directory(
                    child,
                    depth=depth + 1,
                    is_last=child_is_last,
                )

            else:
                yield TraversalEvent(
                    type=TraversalEventType.FILE,
                    path=child,
                    depth=depth + 1,
                    is_last=child_is_last,
                )

        yield TraversalEvent(
            type=TraversalEventType.EXIT_DIRECTORY,
            path=directory,
            depth=depth,
            is_last=is_last,
        )

    def __sort_key(
        self,
        path: Path,
    ) -> tuple[bool, bool, str]:
        return (
            not path.name.startswith("."),
            not path.is_dir(),
            path.name.casefold(),
        )

    def __is_ignored(
        self,
        path: Path,
    ) -> bool:
        try:
            relative = path.relative_to(self.__root).as_posix()

        except ValueError:
            return False

        return self.__spec.match_file(relative)
