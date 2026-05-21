from collections.abc import Generator
from typing import TypeVar

from .dfs_command import DFSCommand
from .dfs_event import DFSEvent

T = TypeVar("T")


type DFSGenerator[T] = Generator[
    DFSEvent[T],
    DFSCommand | None,
    None,
]
