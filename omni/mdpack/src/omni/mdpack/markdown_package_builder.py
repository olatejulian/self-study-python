from pathlib import Path

from .markdown_package_renderer import MarkdownPackageRenderer
from .markdown_render import MarkdownRenderer
from .traversal import PathTraversal, TraversalListener
from .tree_render import TreeRenderer


class MarkdownPackageBuilder:
    def __init__(
        self,
        root: Path,
        ignore_patterns: list[str],
    ) -> None:
        self.__root = root.resolve()

        self.__ignore_patterns = ignore_patterns

    def build(
        self,
    ) -> str:
        traversal = PathTraversal(
            self.__root,
            self.__ignore_patterns,
        )

        tree_renderer = TreeRenderer()

        markdown_renderer = MarkdownRenderer(
            self.__root,
        )

        listeners: list[TraversalListener] = [
            tree_renderer,
            markdown_renderer,
        ]

        for event in traversal.walk():
            for listener in listeners:
                listener.consume(event)

        return MarkdownPackageRenderer(
            self.__root,
            tree_renderer.render(),
            markdown_renderer.render(),
        ).render()
