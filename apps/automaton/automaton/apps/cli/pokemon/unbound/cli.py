from typing import Optional

from typer import Typer

from automaton.apps.cli import common

from ..commands import AddPokemonsFromCsv, GetPokemons
from ..container import build_pokemon_container
from .container import build_unbound_container

unbound_cli = Typer(name="unbound")

unbound_container = build_unbound_container(build_pokemon_container())


@unbound_cli.command()
def add_data(path: str, file_format: str = "csv"):
    match file_format:
        case "csv":
            add_pokemons_from_csv = unbound_container[AddPokemonsFromCsv]

            common.try_run(add_pokemons_from_csv, path=path)


@unbound_cli.command()
def get(
    where: Optional[str] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
):
    get_pokemons = unbound_container[GetPokemons]

    common.try_run(
        get_pokemons,
        query={"where": where, "order_by": order_by, "limit": limit},
    )
