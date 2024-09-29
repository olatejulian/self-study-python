import sqlite3
from typing import Iterator

from ....core import PokeDex, Pokemon, PokemonFactory, Query


class SqliteUnboundNationalPokeDex(PokeDex):
    __insert_query__ = """
    INSERT OR REPLACE INTO
        pokemon_unbound_national_pokedex
    VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """

    __create_table_query__ = """
    CREATE TABLE IF NOT EXISTS
        pokemon_unbound_national_pokedex (
            dex_num INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type_01 TEXT NOT NULL,
            type_02 TEXT NOT NULL,
            hp INTEGER NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            sp_attack INTEGER NOT NULL,
            sp_defense INTEGER NOT NULL,
            speed INTEGER NOT NULL,
            total INTEGER NOT NULL
        );
    """

    @staticmethod
    def __build_query(query: Query):
        base = "select * from pokemon_unbound_national_pokedex"

        if query["where"]:
            base += f" where {query['where']}"

        if query["order_by"]:
            base += f" order by {query['order_by']}"

        if query["limit"]:
            base += f" limit {query['limit']}"

        return base

    def __init__(self, connection: sqlite3.Connection):
        self.__connection = connection

        self.__create_table()

    def __create_table(self):
        with self.__connection as connection:
            cursor = connection.cursor()

            cursor.execute(self.__create_table_query__)

    def add(self, pokemon: Pokemon):
        with self.__connection as connection:
            cursor = connection.cursor()

            values = tuple(pokemon.values())

            cursor.execute(
                self.__insert_query__,
                values,
            )

    def add_many(self, pokemons: list[Pokemon] | Iterator[Pokemon]):
        with self.__connection as connection:
            cursor = connection.cursor()

            values = map(lambda pokemon: tuple(pokemon.values()), pokemons)

            cursor.executemany(
                self.__insert_query__,
                values,
            )

    def get_many(self, query: Query) -> list[Pokemon]:
        with self.__connection as connection:
            cursor = connection.cursor()

            cursor.execute(self.__build_query(query))

            rows = cursor.fetchall()

            return list(map(PokemonFactory.create_from_list, rows))
