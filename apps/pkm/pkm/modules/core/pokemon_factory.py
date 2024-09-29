from typing import Any

from .pokemon import Pokemon


class PokemonFactory:
    @staticmethod
    def create_from_list(values: list[Any]) -> Pokemon:
        return Pokemon(
            dex_number=int(values[0]),
            name=str(values[1]),
            type_01=str(values[2]),
            type_02=str(values[3]),
            hp=int(values[4]),
            attack=int(values[5]),
            defense=int(values[6]),
            sp_attack=int(values[7]),
            sp_defense=int(values[8]),
            speed=int(values[9]),
            total=int(values[10]),
        )
