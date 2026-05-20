from typing import Iterator, Protocol, Self


class Node(Protocol):
    def __iter__(self) -> Iterator[Self]: ...
