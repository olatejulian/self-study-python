from pathlib import Path

from rich.console import Console
from typer import Argument, Exit, Option, Typer

from .directory import Directory
from .formatter_label import LabelFormatterStyle
from .sorting_strategy_factory import SortBy
from .tree_builder_factory import TreeBuilderFactory
from .tree_builder_strategy import (
    TreeBuilderStrategyName,
)

pyls_cli = Typer(name="pyls")


@pyls_cli.command()
def pyls(
    path: str = Argument(".", help="Path to the root directory"),
    reverse: bool = Option(False, help="Reverse sort order"),
    dirs_first: bool = Option(True, help="Directories first"),
    sort_by: SortBy = Option(SortBy.NAME, help="Sort by"),
    label_formatter_style: LabelFormatterStyle = Option(
        LabelFormatterStyle.SIMPLE, help="Label formatter style"
    ),
    tree_builder_method: TreeBuilderStrategyName = Option(
        TreeBuilderStrategyName.MULTI_THREAD, help="Method to build the tree"
    ),
):
    console, console_err = Console(), Console(stderr=True)

    try:
        root_directory = Directory(Path(path))

        tree_builder = TreeBuilderFactory.create(
            reverse,
            dirs_first,
            sort_by,
            label_formatter_style,
            tree_builder_method,
        )

        tree = tree_builder.build(root_directory)

    except:
        console_err.print_exception()

    else:
        console.print(tree)

    finally:
        raise Exit()
