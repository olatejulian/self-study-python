from enum import StrEnum
from typing import Callable

from pyls.traversal.abc_traversal import TraversalStrategy
from pyls.traversal.impl_traversal import BreadthFirstStrategy, DepthFirstStrategy


class TraversalToken(StrEnum):
    DFS = "dfs"
    BFS = "bfs"


di: dict[TraversalToken, Callable[..., TraversalStrategy]] = {
    TraversalToken.DFS: lambda root, callback, max_depth: DepthFirstStrategy(
        root, callback, max_depth
    ),
    TraversalToken.BFS: lambda root, callback, max_depth: BreadthFirstStrategy(
        root, callback, max_depth
    ),
}


def get_traversal(token: TraversalToken, *args, **kwargs) -> TraversalStrategy:
    return di[token](*args, **kwargs)
