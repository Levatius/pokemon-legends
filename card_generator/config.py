from pathlib import Path
from PIL import ImageFont

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR.parent / 'assets'
OUTPUT_DIR = COMPONENT_DIR / 'output'
CARDS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_cards'
TOKENS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_tokens'
CARD_DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_card_decks'
TOKEN_DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_token_decks'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

ART_FORM_URL = 'https://www.serebii.net/pokemon/art'

ORIENTAL_160 = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=160)
BARLOW_80 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=80)
BARLOW_64 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=64)
BARLOW_48 = ImageFont.truetype(str(ASSETS_DIR / 'barlow.ttf'), size=48)

DARK_COLOUR = (37, 37, 50)
WHITE_COLOUR = (255, 255, 255)

CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1717542166339634591/14AF78B5203C3A9A3851A45D7BA0DACA3B19473D/'
DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1717542166339627486/F04352D1A47B673BB72C5D3F50AEA14CC0500C9A/',
    'http://cloud-3.steamusercontent.com/ugc/1717542166339627706/B030B1F98DB2C71871EB5FEA92A5ACD401AA44C4/',
    'http://cloud-3.steamusercontent.com/ugc/1717542166339627897/0B833B49D90F7F6796F9420EFCCC3E802478FB24/',
    'http://cloud-3.steamusercontent.com/ugc/1717542166339628055/BA7CC27B9CC9ABAC3343D110E7FFB4418474CA18/'
]
