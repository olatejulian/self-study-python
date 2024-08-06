from ...text import Text
from .factory import PokemonFactory
from .pokedex import PokeDex, Query


class PokemonService:
    def __init__(self, pokedex: PokeDex):
        self.__pokedex = pokedex

    def add_from_csv(self, file_path: str):
        pokemon_matrix = Text.read_csv(file_path, drop_header=True)

        pokemons = map(
            PokemonFactory.create_from_list,
            pokemon_matrix,
        )

        self.__pokedex.add_many(pokemons)

    def get_many(self, query: Query):
        return self.__pokedex.get_many(query)
