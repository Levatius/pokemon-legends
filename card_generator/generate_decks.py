from PIL import Image

from config import *
from utils import xy, pos


def get_deck_base_img():
    return Image.new('RGBA', pos(10, 7))


def get_deck_output_path(j=0):
    return CARD_DECKS_OUTPUT_DIR / f'{j}_deck.png'


def add_card_at_pos(base_img, pokemon_card_path, position):
    img = Image.open(pokemon_card_path).convert('RGBA').resize(xy(8, 14))
    base_img.paste(img, position, img)
    return base_img


def run():
    pokemon_card_paths = sorted(CARDS_OUTPUT_DIR.glob('*'), key=lambda k: int(k.name.split('_')[0]))

    base_img, output_path = get_deck_base_img(), get_deck_output_path()
    for i, pokemon_card_path in enumerate(pokemon_card_paths):
        j = i // 70
        if j > 0 and i % 70 == 0:
            base_img.save(output_path)
            base_img, output_path = get_deck_base_img(), get_deck_output_path(j)

        base_img = add_card_at_pos(base_img, pokemon_card_path, pos(i % 10, (i // 10) % 7))
    else:
        base_img.save(output_path)
