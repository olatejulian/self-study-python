from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .dfs_context import DFSContext

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DFSEvent(Generic[T]):
    context: DFSContext[T]


@dataclass(slots=True, frozen=True)
class DFSNodeEntered(DFSEvent[T]):
    pass


@dataclass(slots=True, frozen=True)
class DFSNodeExited(DFSEvent[T]):
    pass
