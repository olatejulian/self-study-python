from typer import Typer

from .pdf.cli import pdf_cli
from .pokemon.cli import pokemon
from .series.cli import series
from .subtitle.cli import subtitle_cli

cli = Typer()

cli.add_typer(series)

cli.add_typer(pokemon)

cli.add_typer(pdf_cli)

cli.add_typer(subtitle_cli)
