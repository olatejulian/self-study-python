from abc import ABC, abstractmethod
from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from enum import StrEnum

from rich.tree import Tree

from .directory import Directory
from .file import File
from .filter import Filter
from .formatter_label import LabelFormatter
from .sorting_context import SortingContext


class TreeBuilderStrategy(ABC):
    def __init__(
        self,
        label_formatter: LabelFormatter,
        content_sorter: SortingContext,
        content_filter: Filter,
    ) -> None:
        self._label_formatter = label_formatter
        self._content_sorter = content_sorter
        self._content_filter = content_filter

    @abstractmethod
    def build(self, tree: Tree, directory: Directory) -> None: ...


class TreeBuilderStrategyName(StrEnum):
    NON_RECURSIVE = "non-recursive"
    DEPTH_FIRST = "depth-first"
    BREADTH_FIRST = "breadth-first"
    MULTI_THREAD = "multi-thread"


class TreeBuilderStrategyFactory:
    @staticmethod
    def create(
        builder_name: TreeBuilderStrategyName,
        label_formatter: LabelFormatter,
        content_sorter: SortingContext,
        content_filter: Filter,
    ) -> TreeBuilderStrategy:
        builders: dict[TreeBuilderStrategyName, TreeBuilderStrategy] = {}

        builders[TreeBuilderStrategyName.NON_RECURSIVE] = (
            NonRecursiveTreeBuilderStrategy(
                label_formatter,
                content_sorter,
                content_filter,
            )
        )

        builders[TreeBuilderStrategyName.DEPTH_FIRST] = (
            DepthFirstSearchTreeBuilderStrategy(
                label_formatter,
                content_sorter,
                content_filter,
            )
        )

        builders[TreeBuilderStrategyName.BREADTH_FIRST] = (
            BreadthFirstSearchTreeBuilderStrategy(
                label_formatter,
                content_sorter,
                content_filter,
            )
        )

        builders[TreeBuilderStrategyName.MULTI_THREAD] = (
            MultiThreadSearchTreeBuilderStrategy(
                label_formatter,
                content_sorter,
                content_filter,
            )
        )

        return builders[builder_name]


class NonRecursiveTreeBuilderStrategy(TreeBuilderStrategy):
    def build(self, tree: Tree, directory: Directory) -> None:
        filtered_directory = self._content_filter.apply(directory)

        sorted_directory = self._content_sorter.sort(filtered_directory)

        for content in sorted_directory:
            if isinstance(content, Directory):
                label = self._label_formatter.format_directory_label(content)

                tree.add(label)

            if isinstance(content, File):
                label = self._label_formatter.format_file_label(content)

                tree.add(label)


class DepthFirstSearchTreeBuilderStrategy(TreeBuilderStrategy):
    def build(self, tree: Tree, directory: Directory) -> None:
        filtered_directory = self._content_filter.apply(directory)

        sorted_directory = self._content_sorter.sort(filtered_directory)

        for content in sorted_directory:
            if isinstance(content, Directory):
                label = self._label_formatter.format_directory_label(content)

                branch = tree.add(label)

                self.build(branch, content)

            if isinstance(content, File):
                label = self._label_formatter.format_file_label(content)

                tree.add(label)


class BreadthFirstSearchTreeBuilderStrategy(TreeBuilderStrategy):
    def build(self, tree: Tree, directory: Directory) -> None:
        queue: deque[tuple[Tree, Directory]] = deque()

        queue.append((tree, directory))

        while queue:
            current_tree, current_directory = queue.popleft()

            filtered_directory = self._content_filter.apply(current_directory)

            sorted_directory = self._content_sorter.sort(filtered_directory)

            for content in sorted_directory:
                if isinstance(content, Directory):
                    label = self._label_formatter.format_directory_label(content)

                    branch = current_tree.add(label)

                    queue.append((branch, content))

                if isinstance(content, File):
                    label = self._label_formatter.format_file_label(content)

                    current_tree.add(label)


class MultiThreadSearchTreeBuilderStrategy(TreeBuilderStrategy):
    def build(self, tree: Tree, directory: Directory) -> None:
        futures: list[Future[None]] = []

        with ThreadPoolExecutor() as executor:
            self.__multi_thread_work(directory, tree, futures, executor)

            for future in as_completed(futures):
                future.result()

    def __multi_thread_work(
        self,
        directory: Directory,
        tree: Tree,
        futures: list[Future[None]],
        executor: ThreadPoolExecutor,
    ) -> None:
        filtered_directory = self._content_filter.apply(directory)

        sorted_directory = self._content_sorter.sort(filtered_directory)

        for content in sorted_directory:
            if isinstance(content, Directory):
                label = self._label_formatter.format_directory_label(content)

                branch = tree.add(label)

                future = executor.submit(
                    self.__multi_thread_work,
                    content,
                    branch,
                    futures,
                    executor,
                )

                futures.append(future)

            elif isinstance(content, File):
                label = self._label_formatter.format_file_label(content)

                tree.add(label)
