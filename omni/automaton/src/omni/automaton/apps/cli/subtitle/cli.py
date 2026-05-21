from typer import Typer

from ..common import try_run
from .subtitle import Subtitle

subtitle_cli = Typer(name="subtitle")


@subtitle_cli.command()
def delay(subtitle_path: str, delay: float):
    try_run(Subtitle.delay, subtitle_path=subtitle_path, delay=delay)


@subtitle_cli.command()
def advance(subtitle_path: str, advance: float):
    try_run(Subtitle.advance, subtitle_path=subtitle_path, advance=advance)
