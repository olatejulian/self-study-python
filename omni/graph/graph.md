# graph

## Project Structure

```
graph
├── src
│   └── omni
│   │   └── graph
│   │   │   ├── dfs
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dfs_command.py
│   │   │   │   ├── dfs_context.py
│   │   │   │   ├── dfs_engine.py
│   │   │   │   ├── dfs_event.py
│   │   │   │   ├── dfs_generator.py
│   │   │   │   ├── dfs_invariant.py
│   │   │   │   ├── dfs_validator.py
│   │   │   │   └── dfs_validator_fn.py
│   │   │   ├── __init__.py
│   │   │   └── node.py
├── tests
└── pyproject.toml
```

## File Contents

### src/omni/graph/dfs/__init__.py

```py

```

### src/omni/graph/dfs/dfs_command.py

```py
from typing import Protocol


class DFSCommand(Protocol): ...


class SkipChildren(DFSCommand): ...


class StopTraversal(DFSCommand): ...

```

### src/omni/graph/dfs/dfs_context.py

```py
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

```

### src/omni/graph/dfs/dfs_engine.py

```py
from typing import Generic, TypeVar

from ..node import Node
from .dfs_command import SkipChildren, StopTraversal
from .dfs_context import DFSContext
from .dfs_event import DFSNodeEntered, DFSNodeExited
from .dfs_generator import DFSGenerator
from .dfs_validator import DFSValidator
from .dfs_validator_fn import validate_context

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
                    yield from walk(
                        child, depth=depth + 1, parent=node, path=(*path, child)
                    )

            yield DFSNodeExited(context)

        yield from walk(root, depth=0, parent=None, path=(root,))

```

### src/omni/graph/dfs/dfs_event.py

```py
from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .dfs_context import DFSContext

T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DFSEvent(Generic[T]):
    context: DFSContext[T]


@dataclass(slots=True, frozen=True)
class DFSNodeEntered(DFSEvent[T]):
    pass


@dataclass(slots=True, frozen=True)
class DFSNodeExited(DFSEvent[T]):
    pass

```

### src/omni/graph/dfs/dfs_generator.py

```py
from typing import Generator, TypeAlias, TypeVar

from .dfs_command import DFSCommand
from .dfs_event import DFSEvent

T = TypeVar("T")


DFSGenerator: TypeAlias = Generator[
    DFSEvent[T],
    DFSCommand | None,
    None,
]

```

### src/omni/graph/dfs/dfs_invariant.py

```py
class DFSInvariantError(Exception): ...

```

### src/omni/graph/dfs/dfs_validator.py

```py
"""
DFS traversal invariants.

The DFS engine guarantees:

- depth == len(path) - 1
- path[-1] is node
- parent == path[-2] when parent exists
- root parent is None
- root depth == 0
- discovery_index strictly increases
- entered nodes are exited exactly once
"""

from __future__ import annotations

from typing import Protocol, TypeVar

from .dfs_context import DFSContext
from .dfs_invariant import DFSInvariantError

T = TypeVar("T")


class DFSContextValidator(Protocol[T]):
    def validate(
        self,
        context: DFSContext[T],
    ) -> None: ...


class DFSDepthValidator[T]:
    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        expected_depth = len(context.path) - 1

        if context.depth != expected_depth:
            raise DFSInvariantError(
                (
                    "invalid DFS depth invariant: "
                    f"expected depth={expected_depth}, "
                    f"received depth={context.depth}"
                )
            )


class DFSPathValidator[T]:
    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        if not context.path:
            raise DFSInvariantError("DFS path invariant violated: path is empty")

        if context.path[-1] is not context.node:
            raise DFSInvariantError(
                ("DFS path invariant violated: path does not terminate at current node")
            )


class DFSParentValidator[T]:
    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        if context.parent is None:
            return

        if len(context.path) < 2:
            raise DFSInvariantError(
                ("DFS parent invariant violated: parent exists but path length < 2")
            )

        expected_parent = context.path[-2]

        if expected_parent is not context.parent:
            raise DFSInvariantError(
                (
                    "DFS parent invariant violated: "
                    "parent does not match previous path node"
                )
            )


class DFSRootValidator[T]:
    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        is_root = context.parent is None

        if not is_root:
            return

        if context.depth != 0:
            raise DFSInvariantError(
                ("DFS root invariant violated: root depth must be 0")
            )

        if len(context.path) != 1:
            raise DFSInvariantError(
                ("DFS root invariant violated: root path must contain only root node")
            )


class DFSDiscoveryValidator[T]:
    def __init__(self) -> None:
        self._last_index = -1

    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        if context.discovery_index <= self._last_index:
            raise DFSInvariantError(
                (
                    "DFS discovery invariant violated: "
                    "discovery index must strictly increase"
                )
            )

        self._last_index = context.discovery_index


class DFSValidator[T]:
    def __init__(
        self,
        validators: list[DFSContextValidator[T]] | None = None,
    ) -> None:

        self._validators = (
            validators
            if validators is not None
            else [
                DFSDepthValidator(),
                DFSPathValidator(),
                DFSParentValidator(),
                DFSRootValidator(),
                DFSDiscoveryValidator(),
            ]
        )

    def validate(
        self,
        context: DFSContext[T],
    ) -> None:

        for validator in self._validators:
            validator.validate(context)

```

### src/omni/graph/dfs/dfs_validator_fn.py

```py
"""
DFS traversal invariants.

The DFS engine guarantees:

- depth == len(path) - 1
- path[-1] is node
- parent == path[-2] when parent exists
- root parent is None
- root depth == 0
- discovery_index strictly increases
- entered nodes are exited exactly once
"""

from .dfs_context import DFSContext
from .dfs_invariant import DFSInvariantError


def validate_context[T](
    context: DFSContext[T],
) -> None:

    validate_depth(context)

    validate_path(context)

    validate_parent(context)

    validate_root(context)


def validate_depth[T](
    context: DFSContext[T],
) -> None:

    expected_depth = len(context.path) - 1

    if context.depth != expected_depth:
        raise DFSInvariantError(
            (
                "invalid DFS depth invariant: "
                f"expected depth={expected_depth}, "
                f"received depth={context.depth}"
            )
        )


def validate_path[T](
    context: DFSContext[T],
) -> None:

    if not context.path:
        raise DFSInvariantError("DFS path invariant violated: path is empty")

    if context.path[-1] is not context.node:
        raise DFSInvariantError(
            ("DFS path invariant violated: path does not terminate at current node")
        )


def validate_parent[T](
    context: DFSContext[T],
) -> None:

    if context.parent is None:
        return

    if len(context.path) < 2:
        raise DFSInvariantError(
            ("DFS parent invariant violated: parent exists but path length < 2")
        )

    expected_parent = context.path[-2]

    if expected_parent is not context.parent:
        raise DFSInvariantError(
            ("DFS parent invariant violated: parent does not match previous path node")
        )


def validate_root[T](
    context: DFSContext[T],
) -> None:

    is_root = context.parent is None

    if is_root:
        if context.depth != 0:
            raise DFSInvariantError(
                ("DFS root invariant violated: root depth must be 0")
            )

        if len(context.path) != 1:
            raise DFSInvariantError(
                ("DFS root invariant violated: root path must contain only root node")
            )

```

### src/omni/graph/__init__.py

```py

```

### src/omni/graph/node.py

```py
from typing import Iterator, Protocol, Self


class Node(Protocol):
    def __iter__(self) -> Iterator[Self]: ...

```

### pyproject.toml

```toml
[dependency-groups]
dev = []

[project]
dependencies = []
description = "A graph implementation"

name = "omni-graph"
requires-python = ">=3.12,<3.13"
version = "0.0.0"

```
