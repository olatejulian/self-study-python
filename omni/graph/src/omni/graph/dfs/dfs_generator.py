from collections.abc import Generator
from typing import TypeAlias, TypeVar

from .dfs_command import DFSCommand
from .dfs_event import DFSEvent

T = TypeVar("T")


DFSGenerator: TypeAlias = Generator[
    DFSEvent[T],
    DFSCommand | None,
    None,
]
