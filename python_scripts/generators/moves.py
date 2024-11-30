from pathlib import Path
from PIL import Image, ImageDraw

from python_scripts.config import Paths, Fonts, Colours
from python_scripts.models import Move
from python_scripts.generators.utils import scaled_tuple, extract_colour_from_image, init_apply_methods


class MoveBox:
    def __init__(self, move: Move):
        self.move = move
        self.image: Image = self.generate_image()

    def generate_image(self) -> Image:
        assets = Paths.POKEMON_CARD_ASSETS
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(14.5, 7.5))

        # Background
        apply_image(assets / "move_base", (14.5, 7.5), (0, 0))

        # Type
        apply_image(assets / "types" / self.move.type_, (2, 2), (0.25, 0.25))

        # Name
        font = Fonts.BARLOW.font_variant(size=36)
        apply_text(self.move.name, Colours.ATIUS_BLACK, font, (9.5, 1.75), (7.25, 1.25))

        # Attack Strength
        text = self.move.attack_strength if self.move.attack_strength else "?"
        font = Fonts.LA_ORIENTAL.font_variant(size=44)
        apply_text(text, Colours.ATIUS_BLACK, font, (2, 2), (13.25, 1.25))

        # Effect
        size_cm = (13.5, 3 if self.move.class_ else 4.5)
        position_cm = (7.25, 4 if self.move.class_ else 4.75)
        font = Fonts.BARLOW.font_variant(size=28)
        apply_text(self.move.effect, Colours.ATIUS_BLACK, font, size_cm, position_cm)

        # Class
        if self.move.class_:
            apply_image(assets / "move_classes" / self.move.class_, (14.5, 1.5), (0, 6))

        return base_image


class MoveCard:
    def __init__(self, move: Move):
        self.move = move
        self.image: Image = self.generate_image()

    def generate_image(self) -> Image:
        assets = Paths.POKEMON_CARD_ASSETS
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(16, 28))

        # Background
        apply_image(assets / "card_backs" / "standard", (16, 28), (0, 0))

        # Type Background
        d = ImageDraw.Draw(base_image)
        fill = extract_colour_from_image(assets / "types" / f"{self.move.type_}.png", position=(50, 10))
        d.rectangle([scaled_tuple((0.25, 3.25)), scaled_tuple((15.75, 16.75))], fill)

        # Icon
        apply_image(assets / "move_icon", (12, 8), (2, 6))

        # Banner
        apply_image(assets / "move_banner", (15.5, 3), (0.25, 0.25))

        # Type
        apply_image(assets / "types" / self.move.type_, (2.5, 2.5), (0.5, 0.5))

        # Name
        font = Fonts.BARLOW.font_variant(size=44)
        apply_text(self.move.name, Colours.ATIUS_BLACK, font, (9.25, 2), (3.5, 1.75), "lm", "left")

        # Tuck Banner
        apply_image(assets / "tuck_banner", (15.5, 3.5), (0.25, 15.75))
        font = Fonts.BARLOW.font_variant(size=28)
        apply_text("Tuck under Pokémon when taught", Colours.ATIUS_BLACK, font, (15, 1.75), (8, 17.875))

        # Move
        apply_image(Paths.OUTPUTS / "move_boxes" / self.move.name, (14.5, 7.5), (0.75, 19.75))

        # Move Frame
        apply_image(assets / "move_frame", (16, 10), (0, 18))

        return base_image


# Generators

def generate_move_boxes(moves_list: list, outputs_path: Path, overwrite: bool = True) -> None:
    move_boxes_path = outputs_path / "move_boxes"
    move_boxes_path.mkdir(parents=True, exist_ok=True)

    for i, move in enumerate(moves_list):
        save_path = move_boxes_path / f"{move.name}.png"
        if save_path.is_file() and not overwrite:
            continue
        move_box_image = MoveBox(move).image
        move_box_image.save(save_path)


def generate_move_cards(moves_list: list, outputs_path: Path, overwrite: bool = True) -> None:
    move_cards_path = outputs_path / "move_cards"
    move_cards_path.mkdir(parents=True, exist_ok=True)

    for i, move in enumerate(moves_list):
        save_path = move_cards_path / f"{move.name}.png"
        if save_path.is_file() and not overwrite:
            continue
        move_card_image = MoveCard(move).image
        move_card_image.save(save_path)
