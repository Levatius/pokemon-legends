import urllib.request
from pathlib import Path

from PIL import Image

from python_scripts.config import SEREBII_ART_URL, Paths, Fonts, Colours
from python_scripts.models import Pokemon
from python_scripts.generators.utils import init_apply_methods


class PokemonCard:
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon
        self.image: Image = self.generate_image()

    def generate_image(self) -> Image:
        assets = Paths.POKEMON_CARD_ASSETS
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(16, 28))

        # Background
        background = self._get_background()
        apply_image(assets / "card_bases" / background, (16, 28), (0, 0))

        # Climate/Biome
        climate = self.pokemon.climate if self.pokemon.climate else "unknown"
        apply_image(assets / "climates" / climate, (15.5, 27.5), (0.25, 0.25))
        if self.pokemon.biome:
            apply_image(assets / "biomes" / self.pokemon.biome, (15.5, 27.5), (0.25, 0.25))

        # Frame
        apply_image(assets / "frame_base", (15.5, 19.25), (0.25, 0.25))

        # Pokemon
        pokemon_min_length_cm = 7
        pokemon_max_length_cm = 11 if not self.pokemon.trainer else 9
        pokemon_length_cm = max(min(self.pokemon.total // 2 + 3, pokemon_max_length_cm), pokemon_min_length_cm)
        pokemon_size_cm = (pokemon_length_cm, pokemon_length_cm)
        pokemon_position_cm = ((16 - pokemon_length_cm) / 2, (20 - pokemon_length_cm) / 2)
        for _ in range(2):
            try:
                apply_image(assets / "pokemon" / self.pokemon.pokedex_number, pokemon_size_cm, pokemon_position_cm)
            except FileNotFoundError:
                urllib.request.urlretrieve(
                    url=f"{SEREBII_ART_URL}/{self.pokemon.pokedex_number}.png",
                    filename=assets / "pokemon" / f"{self.pokemon.pokedex_number}.png",
                )
                continue
            else:
                break

        # Trainer
        if self.pokemon.trainer:
            apply_image(assets / "trainers" / self.pokemon.trainer, (5, 9.5), (0, 6.75))

        # Frame Facets
        if not self.pokemon.trainer:
            apply_image(assets / "held_item_bases" / "standard", (3.5, 3.5), (1.75, 12.75))
        apply_image(assets / "stats_bases" / "health", (3.5, 2), (11.75, 7.75))
        apply_image(assets / "stats_bases" / "initiative", (3.5, 2), (11.75, 10.25))

        # Base Types
        for i, type_ in enumerate(self.pokemon.types):
            apply_image(assets / "types" / type_, (2.5, 2.5), (0.5 + i * 2.5, 0.5))

        # Learnable Types
        for i, type_ in enumerate(self.pokemon.learnable_types):
            length_cm = 1.25
            position_cm = (
                3.25 - (len(self.pokemon.learnable_types) / 2 * length_cm) + (i % 2 * length_cm),
                16.75 + i // 2 * length_cm
            )
            apply_image(assets / "types" / type_, (length_cm, length_cm), position_cm)
        if len(self.pokemon.learnable_types) == 0:
            apply_image(assets / "types" / "all", (2.5, 2.5), (0.75, 16.75))

        # Encounter Tier
        apply_image(assets / "encounter_icons" / self.pokemon.encounter_tier, (2, 2), (7, 17))

        # Evolution Icon
        if evolution_icon := self._get_evolution_icon():
            apply_image(assets / "evolution_icons" / evolution_icon, (2.5, 2.5), (12.75, 16.75))

        # Name
        size_cm = (9.25, 1.5 if self.pokemon.description else 2)
        position_cm = (1 + len(self.pokemon.types) * 2.5, 1.75 - (0.5 if self.pokemon.description else 0))
        font = Fonts.BARLOW.font_variant(size=36 if self.pokemon.description else 44)
        apply_text(self.pokemon.pokedex_name, Colours.ATIUS_BLACK, font, size_cm, position_cm, "lm", "left")

        # Description
        if self.pokemon.description:
            position_cm = (1 + len(self.pokemon.types) * 2.5, 2.5)
            font = Fonts.BARLOW.font_variant(size=22)
            apply_text(self.pokemon.description, Colours.ATIUS_BLACK, font, (9.25, 1), position_cm, "lm", "left")

        # Stats
        font = Fonts.LA_ORIENTAL.font_variant(size=44)
        apply_text(self.pokemon.health, Colours.ATIUS_BLACK, font, (1.5, 1.5), (12.75, 8.75))
        apply_text(self.pokemon.initiative, Colours.ATIUS_BLACK, font, (1.5, 1.5), (12.75, 11.25))

        # Evolution Cost
        if self.pokemon.evolve_cost:
            font = Fonts.LA_ORIENTAL.font_variant(size=44)
            apply_text(self.pokemon.evolve_cost, Colours.WHITE, font, (2.5, 2.5), (14, 18))

        # Location Icon
        location_text = " ".join([item for item in ["[compass]", self.pokemon.climate, self.pokemon.biome] if item])
        # apply_image(assets / "compass_icon", (0.75, 0.75), (14.5, 15.5))
        font = Fonts.BARLOW.font_variant(size=20)
        apply_text(location_text, Colours.GREY, font, (4.5, 0.5), (8, 16))

        # Move
        apply_image(Paths.OUTPUTS / "move_boxes" / self.pokemon.signature_move.name, (14.5, 7.5), (0.75, 19.75))

        # Emblem
        vanilla_emblem_path = assets / "emblems" / "vanilla.png"
        emblem = "vanilla" if vanilla_emblem_path.is_file() else "custom"
        apply_image(assets / "emblems" / emblem, (0.5, 0.5), (15, 27))

        return base_image

    def _get_background(self):
        match self.pokemon.encounter_tier:
            case ("grunt", "commander", "boss", "ultra_burst"):
                return "dark"
            case _:
                return "standard"

    def _get_evolution_icon(self):
        if self.pokemon.uncapturable:
            return "uncapturable"
        if not self.pokemon.evolve_into:
            return "final"
        return "standard"


# Generator

def generate_pokemon_cards(pokemon_list: list, outputs_path: Path, overwrite: bool = True) -> None:
    pokemon_cards_path = outputs_path / "pokemon_cards"
    pokemon_cards_path.mkdir(parents=True, exist_ok=True)

    for i, pokemon in enumerate(pokemon_list):
        save_path = pokemon_cards_path / f"{i}.png"
        if save_path.is_file() and not overwrite:
            continue
        pokemon_card_image = PokemonCard(pokemon).image
        pokemon_card_image.save(save_path)
