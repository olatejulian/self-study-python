from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DFSContext(Generic[T]):
    node: T

    depth: int

    parent: T | None

    path: tuple[T, ...]

    discovery_index: int
