from typing import Generic, TypeVar

from ..node import Node
from .dfs_command import SkipChildren, StopTraversal
from .dfs_context import DFSContext
from .dfs_event import DFSNodeEntered, DFSNodeExited
from .dfs_generator import DFSGenerator
from .dfs_validator import DFSValidator

T = TypeVar("T", bound=Node)


class DFSEngine(Generic[T]):
    def __init__(self) -> None:
        self.__validator = DFSValidator[T]()

    def traverse(self, root: T) -> DFSGenerator[T]:
        visited: set[int] = set()

        discovery_index = 0

        def walk(
            node: T, *, depth: int, parent: T | None = None, path: tuple[T, ...]
        ) -> DFSGenerator[T]:
            nonlocal discovery_index

            node_id = id(node)

            if node_id in visited:
                return

            visited.add(node_id)

            context = DFSContext(
                node=node,
                depth=depth,
                parent=parent,
                path=path,
                discovery_index=discovery_index,
            )

            self.__validator.validate(context)

            discovery_index += 1

            command = yield DFSNodeEntered(context)

            if isinstance(command, StopTraversal):
                return

            if not isinstance(command, SkipChildren):
                for child in node:
                    yield from walk(child, depth=depth + 1, parent=node, path=(*path, child))

            yield DFSNodeExited(context)

        yield from walk(root, depth=0, parent=None, path=(root,))
