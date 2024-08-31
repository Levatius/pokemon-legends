from enum import StrEnum

import pandera as pa
from pandera import DataFrameModel, Field


class PokeType(StrEnum):
    TYPELESS = "typeless"
    NORMAL = "normal"
    FIRE = "fire"
    WATER = "water"
    ELECTRIC = "electric"
    GRASS = "grass"
    ICE = "ice"
    FIGHTING = "fighting"
    POISON = "poison"
    GROUND = "ground"
    FLYING = "flying"
    PSYCHIC = "psychic"
    BUG = "bug"
    ROCK = "rock"
    GHOST = "ghost"
    DRAGON = "dragon"
    DARK = "dark"
    STEEL = "steel"
    FAIRY = "fairy"


class Move(DataFrameModel):
    name: str
    type: PokeType
    attack_strength: int
    effect: str


class Pokemon(DataFrameModel):
    pokedex_number: str = Field(coerce=True)
    pokedex_name: str
    internal_name: str
    description: str | None = Field(nullable=True)
    # types: list[PokeType]
    classification: str | None = Field(nullable=True)
    biome: str | None = Field(nullable=True)
    climate: str | None = Field(nullable=True)
    initiative: int
    health: int
    # moves: list[PokeType]
    evolve_into: str
    evolve_cost: int | None = Field(coerce=True, nullable=True)
    # move: Move
    move_name: str
    # move_type: PokeType
    move_attack_strength: int
    move_effect: str
    encounter_tier: str
    trainer: str | None = Field(nullable=True)
    number_in_deck: int
    uncapturable: bool
    state: int | None = Field(nullable=True)

    # @pa.parser("evolve_cost")
    # def cast_to_int(cls, evolve_cost):
    #     return evolve_cost.astype(int)
