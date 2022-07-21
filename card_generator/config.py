from pathlib import Path

# Paths
COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR.parent / 'assets' / 'card_generator'
OUTPUT_DIR = COMPONENT_DIR / 'output'
MOVES_OUTPUT_DIR = OUTPUT_DIR / 'moves'
CARD_FRONTS_OUTPUT_DIR = OUTPUT_DIR / 'card_fronts'
CARD_BACKS_OUTPUT_DIR = OUTPUT_DIR / 'card_backs'
DECKS_OUTPUT_DIR = OUTPUT_DIR / 'decks'
CARD_FRONTS_DECK_IMG = '{j}a_deck.png'
CARD_BACKS_DECK_IMG = '{j}b_deck.png'
DECK_OBJECT_OUTPUT_DIR = OUTPUT_DIR / 'deck_object'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

ART_FORM_URL = 'https://www.serebii.net/pokemon/art'

# Fonts
FONT_DIR = ASSETS_DIR / 'fonts'
ORIENTAL_PATH = str(FONT_DIR / 'la_oriental.otf')
BARLOW_PATH = str(FONT_DIR / 'barlow.ttf')

# Colours
DARK_COLOUR = (37, 37, 50)
WHITE_COLOUR = (255, 255, 255)
