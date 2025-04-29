from rich.tree import Tree

from .directory import Directory
from .formatter_label import LabelFormatter
from .tree_builder_strategy import TreeBuilderStrategy


class TreeBuilderContext:
    def __init__(
        self,
        tree_builder: TreeBuilderStrategy,
        label_formatter: LabelFormatter,
    ):
        self.__tree_builder = tree_builder
        self.__label_formatter = label_formatter

    def build(self, directory: Directory) -> Tree:
        label = self.__label_formatter.format_directory_label(directory)

        tree = Tree(label)

        self.__tree_builder.build(tree, directory)

        return tree
