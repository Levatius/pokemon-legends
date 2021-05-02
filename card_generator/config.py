from pathlib import Path
from PIL import ImageFont

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR / 'assets'
OUTPUT_DIR = COMPONENT_DIR / 'output'
CARDS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_cards'
DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_decks'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

REGULAR_SPRITE_URL = 'https://www.serebii.net/blackwhite/pokemon'
ART_FORM_URL = 'https://www.serebii.net/pokemon/art'
HUGE_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=128)
LARGE_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=96)
MEDIUM_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=64)
SMALL_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=32)
DARK_COLOUR = (37, 37, 50)
WHITE_COLOUR = (255, 255, 255)

NORMAL_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1755817088934009706/72672D0AD43330B3F2FB5128B583DDA2A0D9D7CE/'
NORMAL_DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1778335968028460373/F9514AB3403ABEF1B5845E96C1FC1BDE2B290443/',
    'http://cloud-3.steamusercontent.com/ugc/1778335968028460541/74D4C882CBC45669EDB20E13DC974F8FFAF7DA75/',
    'http://cloud-3.steamusercontent.com/ugc/1778335968028460738/EBAE2DCA5FB2D46E839EC761D0F4EFCBE35E833D/'
]
SHINY_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1755817088934009776/CF6C9FE0321B36BD49BEA860EEB834E38C1E4A04/'
SHINY_DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1778335968028461369/AC6167FC979B05DCAAFEC492F4631ADE78F564F2/',
    'http://cloud-3.steamusercontent.com/ugc/1778335968028461528/1A02D40031648541113C2C625704A9E7967BF246/',
    'http://cloud-3.steamusercontent.com/ugc/1778335968028461681/161C377166602ABF876F30CF0166A43E0999442E/'
]
