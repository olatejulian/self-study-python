from automaton.modules.pokemon import Pokemon, PokemonService, Query

from ..table import ConsoleTable
from .config import POKEMON_TYPES_COLORS, PokedexTableConfig


class AddPokemonsFromCsv:
    def __init__(self, service: PokemonService):
        self.__service = service

    def __call__(self, path: str):
        self.__service.add_from_csv(path)


class GetPokemons:
    @staticmethod
    def __transform_pokemon_attributes(pokemon: Pokemon):
        (
            dex_number,
            name,
            type_01,
            type_02,
            hp,
            attack,
            defense,
            sp_attack,
            sp_defense,
            speed,
            total,
        ) = tuple(map(str, pokemon.values()))

        attributes = [
            dex_number,
            name,
            ConsoleTable.colored_value(POKEMON_TYPES_COLORS[type_01], type_01),
            ConsoleTable.colored_value(POKEMON_TYPES_COLORS[type_02], type_02),
            hp,
            attack,
            defense,
            sp_attack,
            sp_defense,
            speed,
            total,
        ]

        return attributes

    def __init__(self, service: PokemonService, config: PokedexTableConfig):
        self.__service = service
        self.__config = config

    def __call__(self, query: Query):
        pokemons = self.__service.get_many(query)

        table = ConsoleTable(
            title=self.__config.title,
            columns=self.__config.columns,
            data=list(map(self.__transform_pokemon_attributes, pokemons)),
        )

        table.show()
