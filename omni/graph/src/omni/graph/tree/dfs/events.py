from dataclasses import dataclass

from ..node import TreeNode


@dataclass(slots=True, frozen=True)
class DFSEvent[T]:
    node: TreeNode[T]
    depth: int
    index: int
    sequence: int


@dataclass(slots=True, frozen=True)
class NodeEntered[T](DFSEvent[T]): ...


@dataclass(slots=True, frozen=True)
class NodeExited[T](DFSEvent[T]): ...
