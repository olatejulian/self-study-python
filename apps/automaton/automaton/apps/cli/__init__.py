from typer import Typer

from .pdf.cli import pdf_cli
from .pokemon.cli import pokemon
from .series.cli import series

cli = Typer()

cli.add_typer(series)

cli.add_typer(pokemon)

cli.add_typer(pdf_cli)
