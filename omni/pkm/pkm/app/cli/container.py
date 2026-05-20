import sqlite3

from lagom import Container, Singleton

from automaton.modules import sqlite_util

from .config import PokemonCliConfig


def build_pokemon_container(container: Container | None = None) -> Container:
    if not container:
        container = Container()

    container[sqlite3.Connection] = Singleton(
        sqlite_util.get_sqlite_connection(PokemonCliConfig.sqlite_db_path)
    )

    return container
