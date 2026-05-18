from pathlib import Path

from pyls.filtering.di_filtering import FilterToken, get_filter
from pyls.sorting.di_sorting import SortToken, get_sorter
from pyls.traversal.di_traversal import TraversalToken, get_traversal
from pyls.rendering.di_rendering import RendererToken, get_renderer

from typer import Argument, Option, Typer

typer_cli = Typer(name="pyls")


@typer_cli.command()
def pyls(
    path: Path = Argument(
        Path("."),
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=False,
    ),
    sort_by: SortToken = Option(SortToken.NAME, "--sort-by", "-s"),
    ascending: bool = Option(True, "--ascending/--descending"),
    first: bool = Option(True, "--dirs-first/--files-first"),
    hidden: bool = Option(True, "--hidden/--no-hidden"),
    ignore: list[str] = Option([], "--ignore", "-i"),
    gitignore: bool = Option(True, "--gitignore", "-g"),
    depth: int = Option(-1, "--depth", "-d"),
    method: str = Option("breadth-first", "--method", "-m"),
    output: str = Option("rich", "--output", "-o"),
) -> None:


