import rich
from typer import Typer

from .. import common
from . import commands

series = Typer(name="series")


@series.command()
def rename_episodes(path: str):
    common.try_run(
        lambda path: common.generator_handler(
            generator=commands.rename_series_episodes(path),
            mapper=rich.print,
        ),
        path=path,
    )
