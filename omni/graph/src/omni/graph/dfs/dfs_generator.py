from typing import Generator, TypeAlias, TypeVar

from .dfs_command import DFSCommand
from .dfs_event import DFSEvent

T = TypeVar("T")


DFSGenerator: TypeAlias = Generator[
    DFSEvent[T],
    DFSCommand | None,
    None,
]
