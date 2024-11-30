from pathlib import Path

from PIL import ImageFont

SEREBII_ART_URL = "https://www.serebii.net/pokemon/art"

SCALE_FACTOR = 64


class Paths:
    ROOT = Path(__file__).parent.parent
    OUTPUTS = Path(__file__).parent.parent / "outputs"
    POKEMON_CARD_ASSETS = Path(__file__).parent.parent / "assets" / "generators" / "pokemon_cards"


class Fonts:
    BARLOW = ImageFont.truetype(Paths.POKEMON_CARD_ASSETS / "fonts" / "barlow.ttf")
    LA_ORIENTAL = ImageFont.truetype(Paths.POKEMON_CARD_ASSETS / "fonts" / "la_oriental.otf")


class Colours:
    WHITE = (255, 255, 255)
    GREY = (200, 195, 190)
    ATIUS_BLACK = (37, 37, 50)
