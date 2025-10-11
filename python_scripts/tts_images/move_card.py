from pathlib import Path
from PIL import Image, ImageDraw

from python_scripts.config import Paths, Fonts, Colours
from python_scripts.models import Move, TTSImage
from python_scripts.tts_images.utils import scaled_tuple, extract_colour_from_image, init_apply_methods


class MoveCardImage(TTSImage):
    def __init__(self, move: Move, image_path: Path | None = None):
        self.move = move
        self.image: Image.Image = self.cached_image(image_path) if image_path else self.generate_image()

    @property
    def width_cm(self) -> float:
        return 16

    @property
    def height_cm(self) -> float:
        return 28

    def generate_image(self) -> Image:
        assets = Paths.POKEMON_CARD_ASSETS
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(self.width_cm, self.height_cm))

        # Background
        apply_image(assets / "card_backs" / "standard", (self.width_cm, self.height_cm), (0, 0))

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


def generate(moves_list: list, outputs_path: Path, overwrite: bool = True) -> list[MoveCardImage]:
    move_cards_path = outputs_path / "move_cards"
    move_cards_path.mkdir(parents=True, exist_ok=True)

    for i, move in enumerate(moves_list):
        save_path = move_cards_path / f"{move.name}.png"
        if save_path.is_file() and not overwrite:
            move_card = MoveCardImage(move, image_path=save_path)
        else:
            move_card = MoveCardImage(move)
            move_card.image.save(save_path)
        yield move_card
