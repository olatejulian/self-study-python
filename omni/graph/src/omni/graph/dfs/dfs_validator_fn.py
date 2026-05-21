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
            "invalid DFS depth invariant: "
            f"expected depth={expected_depth}, "
            f"received depth={context.depth}"
        )


def validate_path[T](
    context: DFSContext[T],
) -> None:

    if not context.path:
        raise DFSInvariantError("DFS path invariant violated: path is empty")

    if context.path[-1] is not context.node:
        raise DFSInvariantError(
            "DFS path invariant violated: path does not terminate at current node"
        )


def validate_parent[T](
    context: DFSContext[T],
) -> None:

    if context.parent is None:
        return

    if len(context.path) < 2:
        raise DFSInvariantError("DFS parent invariant violated: parent exists but path length < 2")

    expected_parent = context.path[-2]

    if expected_parent is not context.parent:
        raise DFSInvariantError(
            "DFS parent invariant violated: parent does not match previous path node"
        )


def validate_root[T](
    context: DFSContext[T],
) -> None:

    is_root = context.parent is None

    if is_root:
        if context.depth != 0:
            raise DFSInvariantError("DFS root invariant violated: root depth must be 0")

        if len(context.path) != 1:
            raise DFSInvariantError(
                "DFS root invariant violated: root path must contain only root node"
            )
