from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

from .dfs_context import DFSContext

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DFSEvent[T]:
    context: DFSContext[T]


@dataclass(slots=True, frozen=True)
class DFSNodeEntered(DFSEvent[T]):
    pass


@dataclass(slots=True, frozen=True)
class DFSNodeExited(DFSEvent[T]):
    pass
