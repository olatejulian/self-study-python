from __future__ import annotations

from collections.abc import Generator, Iterator
from itertools import count

from ...node import TreeNode
from ..commands import DFSCommand, SkipChildren, StopTraversal
from ..events import DFSEvent, NodeEntered, NodeExited


class PreOrderDFSTraversal[T]:
    def traverse(self, node: TreeNode[T]) -> Generator[DFSEvent[T], DFSCommand | None, None]:
        sequence_counter = count()

        yield from self._walk(node=node, depth=0, index=0, sequence=sequence_counter)

        return

    def _walk(
        self, node: TreeNode[T], depth: int, index: int, sequence: Iterator[int]
    ) -> Generator[DFSEvent[T], DFSCommand | None, None]:
        current_sequence = next(sequence)

        command = yield NodeEntered(node=node, depth=depth, index=index, sequence=current_sequence)

        if isinstance(command, StopTraversal):
            return

        if not isinstance(command, SkipChildren):
            for child_index, child in enumerate(node.children()):
                yield from self._walk(child, depth + 1, child_index, sequence)

        command = yield NodeExited(node=node, depth=depth, index=index, sequence=current_sequence)

        if isinstance(command, StopTraversal):
            return
