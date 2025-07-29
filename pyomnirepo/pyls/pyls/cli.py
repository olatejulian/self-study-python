from pathlib import Path

from rich.console import Console
from typer import Argument, Exit, Option, Typer

from .list_directory_content_handler import ListDirectoryContentHandler
from .sorting_strategy_factory import SortBy

pyls_cli = Typer(name="pyls")


@pyls_cli.command()
def pyls(
    path: Path = Argument(
        default=Path("."),
        help="Path to the root directory",
    ),
    recursive: bool = Option(
        False,
        *["--recursive", "-r"],
        help="Recursively list directory contents",
    ),
    hidden: bool = Option(
        False,
        *["--hidden", "-h"],
        help="Show hidden directory contents",
    ),
    ignored: bool = Option(
        False,
        *["--ignored", "-i"],
        help="do not show ignored contents from .gitignore",
    ),
    sort_by: SortBy = Option(
        SortBy.NAME,
        *["--sort-by", "-s"],
        help="Select sort by option",
    ),
):
    console, console_err = Console(), Console(stderr=True)

    try:
        tree = ListDirectoryContentHandler.execute(
            path=path,
            recursive=recursive,
            hidden=hidden,
            ignored=ignored,
            sort_by=sort_by,
        )

    except:
        console_err.print_exception()

    else:
        console.print(tree)

    finally:
        raise Exit()
