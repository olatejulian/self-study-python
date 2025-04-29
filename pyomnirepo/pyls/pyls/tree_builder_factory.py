from .formatter_label import LabelFormatterFactory, LabelFormatterStyle
from .sorting_context import DefaultSortingContext, SortingContext
from .sorting_strategy_factory import SortBy, SortByStrategyFactory
from .tree_builder_context import TreeBuilderContext
from .tree_builder_strategy import (
    TreeBuilderStrategyFactory,
    TreeBuilderStrategyName,
)


class TreeBuilderFactory:
    @staticmethod
    def create(
        reverse: bool,
        dirs_first: bool,
        sort_by: SortBy,
        label_formatter_style: LabelFormatterStyle,
        tree_builder_method: TreeBuilderStrategyName,
    ) -> TreeBuilderContext:
        label_formatter = LabelFormatterFactory.create(label_formatter_style)

        sort_by_strategy = SortByStrategyFactory.create(sort_by)

        sort_by_context: SortingContext = DefaultSortingContext(
            sort_by_strategy, reverse, dirs_first
        )

        tree_builder_strategy = TreeBuilderStrategyFactory.create(
            tree_builder_method, label_formatter, sort_by_context
        )

        tree_builder_context = TreeBuilderContext(
            tree_builder_strategy, label_formatter
        )

        return tree_builder_context
