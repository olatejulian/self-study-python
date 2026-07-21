from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class TreeNode[T](Protocol):
    value: T
    parent: "TreeNode[T] | None"

    def children(self) -> Iterable["TreeNode[T]"]: ...
