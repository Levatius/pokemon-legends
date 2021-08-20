from pathlib import Path
from PIL import ImageFont

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR.parent / 'assets'
OUTPUT_DIR = COMPONENT_DIR / 'output'
CARDS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_cards'
CARD_DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_card_decks'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

ART_FORM_URL = 'https://www.serebii.net/pokemon/art'

ORIENTAL_160 = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=160)
BARLOW_96 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=96)
BARLOW_80 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=80)
BARLOW_64 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=64)
BARLOW_48 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=48)

DARK_COLOUR = (37, 37, 50)
WHITE_COLOUR = (255, 255, 255)

STANDARD_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1717542408497689638/14AF78B5203C3A9A3851A45D7BA0DACA3B19473D/'
PERFECT_WORLD_ORDER_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1695025250441629233/2C1456E366D0C8B7C49CF659542814A3AD55D92B/'
DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1691651067504980915/45E267964DE7D8DB00B34B4B53234E92D91DA03E/',
    'http://cloud-3.steamusercontent.com/ugc/1691651067504981092/7C1A9F9CB7152F7BFD9E3FAB557D69C04D3B8132/',
    'http://cloud-3.steamusercontent.com/ugc/1691651067504981277/2DB8637439EEF7B40A9D10B0DA966711B77A0057/',
    'http://cloud-3.steamusercontent.com/ugc/1691651067504981435/8D4F885DF3D4B4402CF3C9EF02AFAAD64F34A174/'
]
