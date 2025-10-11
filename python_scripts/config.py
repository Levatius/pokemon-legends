from pathlib import Path

from PIL import ImageFont

_ROOT = Path(__file__).parent.parent
SEREBII_ART_URL = "https://www.serebii.net/pokemon/art"
SCALE_FACTOR = 64


class Paths:
    ROOT = _ROOT
    OUTPUTS = _ROOT / "outputs"
    POKEMON_CARD_ASSETS = _ROOT / "assets" / "generators" / "pokemon_cards"

class Fonts:
    BARLOW = ImageFont.truetype(Paths.POKEMON_CARD_ASSETS / "fonts" / "barlow.ttf")
    LA_ORIENTAL = ImageFont.truetype(Paths.POKEMON_CARD_ASSETS / "fonts" / "la_oriental.otf")


class Colours:
    WHITE = (255, 255, 255)
    GREY = (200, 195, 190)
    ATIUS_BLACK = (37, 37, 50)
