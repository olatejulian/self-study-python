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
    path: Path = Argument(Path("."), help="Path to the root directory"),
    reverse: bool = Option(False, help="Reverse sort order"),
    dirs_first: bool = Option(True, help="Directories first"),
    ignore_contents: list[str] = Option(
        [], "--ignore", "-I", help="Content filter"
    ),
    ignore_contents_from_file: Path = Option(
        Path(".gitignore"), "--file-ignore", "-F", help="Content filter file"
    ),
    sort_by: SortBy = Option(SortBy.NAME, "--sort-by", "-S", help="Sort by"),
    label_style: LabelFormatterStyle = Option(
        LabelFormatterStyle.SIMPLE,
        "--label-style",
        "-L",
        help="Label style",
    ),
    tree_builder_method: TreeBuilderStrategyName = Option(
        TreeBuilderStrategyName.MULTI_THREAD,
        "--tree-builder-method",
        "-T",
        help="Method to build the tree",
    ),
):
    console, console_err = Console(), Console(stderr=True)

    try:
        root_directory = Directory(Path(path))

        if (
            ignore_contents_from_file.exists()
            and ignore_contents_from_file.is_file()
        ):
            ignore_contents.extend(
                ignore_contents_from_file.read_text("utf-8").splitlines()
            )

        tree_builder = TreeBuilderFactory.create(
            reverse,
            dirs_first,
            sort_by,
            ignore_contents,
            label_style,
            tree_builder_method,
        )

        tree = tree_builder.build(root_directory)

    except:
        console_err.print_exception()

    else:
        console.print(tree)

    finally:
        raise Exit()
