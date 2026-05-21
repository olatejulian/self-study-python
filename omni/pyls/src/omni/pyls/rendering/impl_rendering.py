from pathlib import Path
from typing import Union

from rich.console import Console
from rich.tree import Tree

from omni.pyls.src.omni.pyls.traversal.impl_traversal import (
    BreadthTraversalEvent,
    BreadthTraversalState,
    DepthTraversalEvent,
    DepthTraversalState,
)

# We unify event interface for simplicity:
TraversalEvent = Union[DepthTraversalEvent, BreadthTraversalEvent]


class RichTreeRenderer:
    """
    Renderer that produces a visual tree using rich.
    Expects traversal events in a sequence of:
        ENTER_DIR, FILE, EXIT_DIR.
    """

    def __init__(self, *, clear_console: bool = False) -> None:
        self.console = Console()
        self._stack: list[Tree] = []
        self._root_tree: Tree | None = None
        self._clear = clear_console

    def render(self, event: TraversalEvent) -> None:
        """
        Render a single event.
        """
        # Dispatch based on event.state
        state = event.state

        # Directory entered
        if state is DepthTraversalState.ENTER_DIR or state is BreadthTraversalState.ENTER_DIR:
            self._enter_dir(event.path, event.depth)

        # File
        elif state is DepthTraversalState.FILE or state is BreadthTraversalState.FILE:
            self._file(event.path, event.depth)

        # Directory exit
        elif state is DepthTraversalState.EXIT_DIR or state is BreadthTraversalState.EXIT_DIR:
            self._exit_dir()

    def _enter_dir(self, path: Path, depth: int) -> None:
        """
        Called when a directory is entered.
        """
        # Label with directory icon and name
        label = f"📁 {path.name}"

        if depth == 0:
            # Root directory, create root tree
            self._root_tree = Tree(label)
            self._stack.append(self._root_tree)
        else:
            parent = self._stack[-1]
            branch = parent.add(label)
            self._stack.append(branch)

    def _file(self, path: Path, depth: int) -> None:
        """
        Called for file events.
        """
        label = f"📄 {path.name}"

        if not self._stack:
            # If no current stack, we just print directly
            self.console.print(label)
        else:
            parent = self._stack[-1]
            parent.add(label)

    def _exit_dir(self) -> None:
        """
        Pop current directory branch.
        """
        if len(self._stack) > 1:
            self._stack.pop()

    def finalize(self) -> None:
        """
        Must be called after traversal to print the tree to console.
        """
        if self._root_tree is not None:
            if self._clear:
                self.console.clear()
            self.console.print(self._root_tree)
