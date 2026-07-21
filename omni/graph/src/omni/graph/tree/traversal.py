from collections.abc import Generator
from typing import Protocol, TypeVar

N = TypeVar("N", contravariant=True)
E = TypeVar("E", covariant=True)
C = TypeVar("C", contravariant=True)
R = TypeVar("R", covariant=True)


class Traversal[N, E, C, R](Protocol):
    def traverse(self, node: N) -> Generator[E, C, R]: ...
