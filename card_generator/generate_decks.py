import pandas as pd
from PIL import Image

from config import *
from utils import xy, pos, read_cube

CARD_FRONTS_DECK_IMG = '{j}_card_fronts_deck.png'
CARD_BACKS_DECK_IMG = '{j}_card_backs_deck.png'


def get_card_deck_base_img():
    return Image.new('RGBA', pos(10, 7))


def add_card_at_pos(base_img, pokemon_card_path, position):
    img = Image.open(pokemon_card_path).convert('RGBA').resize(xy(8, 14))
    base_img.paste(img, position, img)
    return base_img


def run():
    i, j = 0, 0
    df = read_cube()

    card_fronts_deck_img = get_card_deck_base_img()
    card_backs_deck_img = get_card_deck_base_img()

    for row_number, stats in df.iterrows():
        if i == 70:
            card_fronts_deck_img.save(DECKS_OUTPUT_DIR / CARD_FRONTS_DECK_IMG.format(j=j))
            card_fronts_deck_img = get_card_deck_base_img()
            card_backs_deck_img.save(DECKS_OUTPUT_DIR / CARD_BACKS_DECK_IMG.format(j=j))
            card_backs_deck_img = get_card_deck_base_img()
            i = 0
            j += 1

        pokemon_card_path = CARD_FRONTS_OUTPUT_DIR / f'{row_number}_{stats.pokedex_name}.png'
        card_back_path = CARD_BACKS_OUTPUT_DIR / f'{stats.move_name}.png' if pd.isnull(
            stats.trainer) else ASSETS_DIR / 'card_backs' / 'galactic.png'
        card_pos = pos(i % 10, (i // 10) % 7)

        card_fronts_deck_img = add_card_at_pos(card_fronts_deck_img, pokemon_card_path, card_pos)
        card_backs_deck_img = add_card_at_pos(card_backs_deck_img, card_back_path, card_pos)
        i += 1
    else:
        card_fronts_deck_img.save(DECKS_OUTPUT_DIR / CARD_FRONTS_DECK_IMG.format(j=j))
        card_backs_deck_img.save(DECKS_OUTPUT_DIR / CARD_BACKS_DECK_IMG.format(j=j))


if __name__ == '__main__':
    run()
