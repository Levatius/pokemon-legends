from pathlib import Path

from PIL import Image

from python_scripts.models import TTSImage
from python_scripts.tts_images.utils import init_apply_methods, scaled_tuple

MAX_DECK_WIDTH = 10
MAX_DECK_HEIGHT = 7
MAX_DECK_SIZE = MAX_DECK_WIDTH * MAX_DECK_HEIGHT


class DeckImage(TTSImage):
    def __init__(self, deck_id: int, card_images: list[TTSImage], image_path: Path | None = None):
        self.id = deck_id
        self.cards = card_images
        assert 0 < len(card_images) <= MAX_DECK_SIZE  # Max allowed cards in a TTS deck image is 70
        self.image: Image.Image = self.cached_image(image_path) if image_path else self.generate_image()
        self.url = None  # The URL is populated after the upload of the deck image to TTS

    @property
    def width_cm(self) -> float:
        sample_card = self.cards[0]
        return sample_card.width_cm * MAX_DECK_WIDTH  # Max 10 cards in a row

    @property
    def height_cm(self) -> float:
        sample_card = self.cards[0]
        return sample_card.height_cm * MAX_DECK_HEIGHT  # Max 7 cards in a column

    def generate_image(self) -> Image.Image:
        base_image, apply_image, apply_text = init_apply_methods(base_size_cm=(self.width_cm, self.height_cm))

        for i, card in enumerate(self.cards):
            row_number = i // MAX_DECK_WIDTH
            column_number = i % MAX_DECK_WIDTH
            position_cm = (card.width_cm * column_number, card.height_cm * row_number)
            apply_image(card.image, (card.width_cm, card.height_cm), position_cm)

        rescaled_size = scaled_tuple((self.width_cm // 2, self.height_cm // 2))
        return base_image.resize(rescaled_size)


def generate(card_images: list[TTSImage], outputs_path: Path, overwrite: bool = True) -> list[DeckImage]:
    outputs_path.mkdir(parents=True, exist_ok=True)

    total_decks = (len(card_images) // MAX_DECK_SIZE) + 1
    for i in range(total_decks):
        deck_id = i + 1 # Deck IDs start at 1 in TTS
        save_path = outputs_path / f"{deck_id}.png"
        deck_card_images = card_images[MAX_DECK_SIZE * i:MAX_DECK_SIZE * (i + 1)]
        if save_path.is_file() and not overwrite:
            deck = DeckImage(deck_id, deck_card_images, image_path=save_path)
        else:
            deck = DeckImage(deck_id, deck_card_images)
            deck.image.save(save_path)
        yield deck
