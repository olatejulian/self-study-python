import sqlite3

from lagom import Container

from automaton.modules.pokemon import (
    PokeDex,
    PokemonService,
    SqliteUnboundNationalPokeDex,
)

from ..commands import AddPokemonsFromCsv, GetPokemons
from ..config import PokedexTableConfig
from .config import UnboundTableConfig


def build_unbound_container(container: Container | None = None) -> Container:
    if not container:
        container = Container()

    container[PokeDex] = lambda c: SqliteUnboundNationalPokeDex(
        c[sqlite3.Connection]
    )

    container[PokemonService] = lambda c: PokemonService(c[PokeDex])

    container[AddPokemonsFromCsv] = lambda c: AddPokemonsFromCsv(
        c[PokemonService]
    )

    container[PokedexTableConfig] = UnboundTableConfig()

    container[GetPokemons] = lambda c: GetPokemons(
        c[PokemonService], c[PokedexTableConfig]
    )

    return container
