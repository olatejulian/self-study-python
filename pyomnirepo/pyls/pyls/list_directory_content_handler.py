from pathlib import Path

from rich.tree import Tree

from .directory import Directory
from .filter import Filter
from .formatter_label import LabelFormatterFactory, LabelFormatterStyle
from .sorting_context import DefaultSortingContext, SortingContext
from .sorting_strategy_factory import SortBy, SortByStrategyFactory
from .tree_builder_context import TreeBuilderContext
from .tree_builder_strategy import (
    TreeBuilderStrategyFactory,
    TreeBuilderStrategyName,
)


class ListDirectoryContentHandler:
    @staticmethod
    def execute(
        path: Path = Path("."),
        recursive: bool = False,
        hidden: bool = False,
        ignored: bool = True,
        sort_by: SortBy = SortBy.NAME,
    ) -> Tree:
        root_directory = Directory(path)

        label_formatter = LabelFormatterFactory.create(style=LabelFormatterStyle.SIMPLE)

        sort_by_strategy = SortByStrategyFactory.create(sort_by=sort_by)

        sort_by_context: SortingContext = DefaultSortingContext(
            sort_by_strategy=sort_by_strategy, reverse=False, dirs_first=True
        )

        if ignored:
            gitignore_path = path.resolve() / Path(".gitignore")

            if gitignore_path.resolve().exists():
                ignored_contents = gitignore_path.read_text().splitlines()

                content_filter = Filter(words=ignored_contents)

            else:
                content_filter = Filter(words=[])

        else:
            content_filter = Filter(words=[])

        if recursive:
            builder_name = TreeBuilderStrategyName.MULTI_THREAD

        else:
            builder_name = TreeBuilderStrategyName.NON_RECURSIVE

        tree_builder_strategy = TreeBuilderStrategyFactory.create(
            builder_name=builder_name,
            label_formatter=label_formatter,
            content_sorter=sort_by_context,
            content_filter=content_filter,
        )

        tree_builder = TreeBuilderContext(
            tree_builder=tree_builder_strategy, label_formatter=label_formatter
        )

        tree = tree_builder.build(root_directory)

        return tree
