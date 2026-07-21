from collections.abc import Generator

from omni.graph.tree.dfs.commands import DFSCommand
from omni.graph.tree.dfs.events import DFSEvent
from omni.graph.tree.node import TreeNode


class PostOrderDFSTraversal[T]:
    def traverse(self, node: TreeNode[T]) -> Generator[DFSEvent[T], DFSCommand | None, None]: ...
