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
