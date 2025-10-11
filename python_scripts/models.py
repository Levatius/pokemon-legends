from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Protocol

import pandera as pa
from pandera import DataFrameModel, Field
from PIL import Image

from python_scripts.tts_images.utils import load_image, scaled_tuple


# class PokeType(StrEnum):
#     TYPELESS = "typeless"
#     NORMAL = "normal"
#     FIRE = "fire"
#     WATER = "water"
#     ELECTRIC = "electric"
#     GRASS = "grass"
#     ICE = "ice"
#     FIGHTING = "fighting"
#     POISON = "poison"
#     GROUND = "ground"
#     FLYING = "flying"
#     PSYCHIC = "psychic"
#     BUG = "bug"
#     ROCK = "rock"
#     GHOST = "ghost"
#     DRAGON = "dragon"
#     DARK = "dark"
#     STEEL = "steel"
#     FAIRY = "fairy"

class TTSImage(Protocol):
    image: Image

    @property
    def width_cm(self) -> float:
        ...

    @property
    def height_cm(self) -> float:
        ...

    def cached_image(self, image_path: Path) -> Image.Image:
        return load_image(image_path, size=scaled_tuple((self.width_cm, self.height_cm)))

    def generate_image(self) -> Image.Image:
        ...

class TTSObject(Protocol):
    @property
    def nickname(self) -> str | None:
        """
        Default name shown on the card in TTS.
        """
        ...

    @property
    def description(self) -> str | None:
        """
        Description shown when hovering over the card in TTS.
        """
        ...

    @property
    def tags(self) -> list[str]:
        """
        All tags on the card in TTS.
        """
        ...

    @property
    def lua_script(self) -> str | None:
        ...


class PokemonDataModel(DataFrameModel):
    pokedex_number: str = Field(coerce=True)
    pokedex_name: str
    internal_name: str
    description: str = Field(nullable=True)
    type_1: str
    type_2: str = Field(nullable=True)
    classification: str = Field(nullable=True)
    biome: str = Field(nullable=True)
    climate: str = Field(nullable=True)
    initiative: int = Field(coerce=True)
    health: int = Field(coerce=True)
    total: int = Field(coerce=True)
    move_1: str = Field(nullable=True)
    move_2: str = Field(nullable=True)
    move_3: str = Field(nullable=True)
    move_4: str = Field(nullable=True)
    evolve_into: str = Field(nullable=True)
    evolve_cost: int = Field(nullable=True)
    move_name: str
    move_type: str
    move_attack_strength: int = Field(nullable=True)
    move_class: str = Field(nullable=True)
    move_effect: str
    encounter_tier: str
    trainer: str = Field(nullable=True)
    number_in_deck: int
    uncapturable: bool = Field(coerce=True)
    state: int = Field(nullable=True)

    @pa.parser("pokedex_number")
    def zfill_pokedex_number(self, series):
        def parser(pokedex_number):
            split_pokedex_number = pokedex_number.split("-")
            split_pokedex_number[0] = split_pokedex_number[0].zfill(3)
            return "-".join(split_pokedex_number)

        return series.apply(parser)

    @pa.parser("evolve_cost", "move_attack_strength", "state")
    def cast_to_nullable_int(self, series):
        return series.astype("Int64")

    class Config:
        strict = "filter"


class MovesDataModel(DataFrameModel):
    move_name: str = Field(unique=True)
    move_type: str
    move_attack_strength: int = Field(nullable=True)
    move_class: str = Field(nullable=True)
    move_effect: str

    @pa.parser("move_attack_strength")
    def cast_to_nullable_int(self, series):
        return series.astype("Int64")

    class Config:
        strict = "filter"


@dataclass
class Move:
    name: str
    type_: str
    attack_strength: int | None
    class_: str
    effect: str

    @classmethod
    def from_df_row(cls, row):
        return cls(
            name=row.move_name,
            type_=row.move_type,
            attack_strength=row.move_attack_strength,
            class_=row.move_class,
            effect=row.move_effect,
        )


@dataclass
class Pokemon:
    pokedex_number: str
    pokedex_name: str
    internal_name: str
    description: str
    types: list[str]
    classification: str
    biome: str
    climate: str
    initiative: int
    health: int
    total: int
    learnable_types: list[str]
    evolve_into: list[str] | None
    evolve_cost: int | None
    signature_move: Move
    encounter_tier: str
    trainer: str | None
    number_in_deck: int
    uncapturable: bool
    state: int

    @classmethod
    def from_df_row(cls, row):
        return cls(
            pokedex_number=row.pokedex_number,
            pokedex_name=row.pokedex_name,
            internal_name=row.internal_name,
            description=row.description,
            types=[type_ for type_ in (row.type_1, row.type_2) if type_],
            classification=row.classification,
            biome=row.biome,
            climate=row.climate,
            initiative=row.initiative,
            health=row.health,
            total=row.total,
            learnable_types=[move for move in (row.move_1, row.move_2, row.move_3, row.move_4) if move],
            evolve_into=row.evolve_into.split("/") if row.evolve_into else None,
            evolve_cost=row.evolve_cost,
            signature_move=Move(
                name=row.move_name,
                type_=row.move_type,
                attack_strength=row.move_attack_strength,
                class_=row.move_class,
                effect=row.move_effect,
            ),
            encounter_tier=row.encounter_tier,
            trainer=row.trainer,
            number_in_deck=row.number_in_deck,
            uncapturable=row.uncapturable,
            state=row.state,
        )
