from typer import Typer

from .unbound import unbound_cli

pokemon = Typer(name="pokemon")

pokemon.add_typer(unbound_cli)
