from __future__ import annotations

from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DFSContext[T]:
    node: T

    depth: int

    parent: T | None

    path: tuple[T, ...]

    discovery_index: int
