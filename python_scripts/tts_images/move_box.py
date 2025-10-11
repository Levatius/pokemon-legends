from pathlib import Path
from PIL import Image

from python_scripts.config import Paths, Fonts, Colours
from python_scripts.models import Move, TTSImage
from python_scripts.tts_images.utils import init_apply_methods


class MoveBoxImage(TTSImage):
    def __init__(self, move: Move, image_path: Path | None = None):
        self.move = move
        self.image: Image.Image = self.cached_image(image_path) if image_path else self.generate_image()

    @property
    def width_cm(self) -> float:
        return 14.5

    @property
    def height_cm(self) -> float:
        return 7.5

    def generate_image(self) -> Image:
        assets = Paths.POKEMON_CARD_ASSETS
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(self.width_cm, self.height_cm))

        # Background
        apply_image(assets / "move_base", (self.width_cm, self.height_cm), (0, 0))

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


def generate(moves_list: list, outputs_path: Path, overwrite: bool = True) -> list[MoveBoxImage]:
    move_boxes_path = outputs_path / "move_boxes"
    move_boxes_path.mkdir(parents=True, exist_ok=True)

    for i, move in enumerate(moves_list):
        save_path = move_boxes_path / f"{move.name}.png"
        if save_path.is_file() and not overwrite:
            move_box = MoveBoxImage(move, image_path=save_path)
        else:
            move_box = MoveBoxImage(move)
            move_box.image.save(save_path)
        yield move_box
