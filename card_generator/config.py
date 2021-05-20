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
    'http://cloud-3.steamusercontent.com/ugc/1787345070256771885/F7DDBED0D4BF47F6A17E3F4FC35784F0D445A91C/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256772083/72E7DFED1BED6566E550DA7C9CC0DA67ED9FD8C3/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256772250/C5FA8340B6E513E1EF64FE9F6AE1E3C42D317F79/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256772375/67C7582AF102607F017BFD3E361C2FCB340C6C7F/'
]
SHINY_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1755817088934009776/CF6C9FE0321B36BD49BEA860EEB834E38C1E4A04/'
SHINY_DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1787345070256774731/DF3D4242C3F76879CF5AAD8E61E373AB3CC7513A/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256774882/A7A0B9661E1E0A2F6FDFF65C004367C627938F89/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256775229/50105F067782EBCEA65CDD99D48490B37537C2B2/',
    'http://cloud-3.steamusercontent.com/ugc/1787345070256775368/95F80E8479CA8555259C4B096A9B769FAA09408E/'
]
