from typing import TypedDict


class Pokemon(TypedDict):
    dex_number: int
    name: str
    type_01: str
    type_02: str
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    total: int
