from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Callable, Deque, Iterable, Iterator, Optional

from omni.pyls.src.omni.pyls.traversal.abc_traversal import TraversalStrategy

Callback = Callable[[Path], Iterable[Path]]


class DepthTraversalState(Enum):
    ENTER_DIR = auto()
    EXIT_DIR = auto()
    FILE = auto()


@dataclass(frozen=True)
class DepthTraversalEvent:
    path: Path
    state: DepthTraversalState
    depth: int


class DepthFirstStrategy(TraversalStrategy[DepthTraversalEvent]):
    def __init__(
        self,
        root: Path,
        callback: Callback,
        max_depth: int,
    ) -> None:
        self._stack: list[
            tuple[Path, Optional[Iterator[Path]], int, DepthTraversalState]
        ] = [(root, None, 0, DepthTraversalState.ENTER_DIR)]
        self._callback = callback
        self._max_depth = max_depth

    def __iter__(self):
        return self

    def __next__(self) -> DepthTraversalEvent:
        while self._stack:
            node, children_iter, depth, state = self._stack.pop()

            # ENTER_DIR
            if state is DepthTraversalState.ENTER_DIR:
                # schedule exit
                self._stack.append((node, None, depth, DepthTraversalState.EXIT_DIR))

                # schedule children iterator
                if self._max_depth < 0 or depth < self._max_depth:
                    children_iter = iter(self._callback(node))
                    self._stack.append(
                        (node, children_iter, depth, DepthTraversalState.FILE)
                    )
                return DepthTraversalEvent(node, DepthTraversalState.ENTER_DIR, depth)

            # CHILDREN iterator handler
            if children_iter is not None:
                try:
                    child = next(children_iter)
                except StopIteration:
                    continue

                # push back same iterator
                self._stack.append(
                    (node, children_iter, depth, DepthTraversalState.FILE)
                )

                # now schedule child
                if child.is_dir():
                    self._stack.append(
                        (child, None, depth + 1, DepthTraversalState.ENTER_DIR)
                    )
                else:
                    return DepthTraversalEvent(
                        child, DepthTraversalState.FILE, depth + 1
                    )
                continue

            # EXIT_DIR
            if state is DepthTraversalState.EXIT_DIR:
                return DepthTraversalEvent(node, DepthTraversalState.EXIT_DIR, depth)

        raise StopIteration


class BreadthTraversalState(Enum):
    ENTER_DIR = auto()
    EXIT_DIR = auto()
    FILE = auto()


@dataclass(frozen=True)
class BreadthTraversalEvent:
    path: Path
    state: BreadthTraversalState
    depth: int


class BreadthFirstStrategy(TraversalStrategy[BreadthTraversalEvent]):
    def __init__(self, root: Path, callback: Callback, max_depth: int) -> None:
        self._queue: Deque[tuple[Path, int]] = deque([(root, 0)])
        self._callback = callback
        self._max_depth = max_depth

        self._pending_files: Deque[BreadthTraversalEvent] = deque()
        self._pending_exit: BreadthTraversalEvent | None = None

    def __iter__(self):
        return self

    def __next__(self) -> BreadthTraversalEvent:
        if self._pending_files:
            return self._pending_files.popleft()

        if self._pending_exit:
            ev = self._pending_exit
            self._pending_exit = None
            return ev

        if not self._queue:
            raise StopIteration

        node, depth = self._queue.popleft()

        # Schedule EXIT
        self._pending_exit = BreadthTraversalEvent(
            node, BreadthTraversalState.EXIT_DIR, depth
        )

        # Collect children
        if self._max_depth < 0 or depth < self._max_depth:
            for child in self._callback(node):
                if child.is_dir():
                    self._queue.append((child, depth + 1))
                else:
                    self._pending_files.append(
                        BreadthTraversalEvent(
                            child, BreadthTraversalState.FILE, depth + 1
                        )
                    )

        return BreadthTraversalEvent(node, BreadthTraversalState.ENTER_DIR, depth)
