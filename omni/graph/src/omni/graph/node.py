from collections.abc import Iterator
from typing import Protocol, Self


class Node(Protocol):
    def __iter__(self) -> Iterator[Self]: ...
