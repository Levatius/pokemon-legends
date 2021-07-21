from PIL import Image

from config import *
from utils import xy, pos, read_cube, is_trainer_deck_boundary


def get_deck_base_img():
    return Image.new('RGBA', pos(10, 7))


def get_deck_output_path(j=0):
    return CARD_DECKS_OUTPUT_DIR / f'{j}_deck.png'


def add_card_at_pos(base_img, pokemon_card_path, position):
    img = Image.open(pokemon_card_path).convert('RGBA').resize(xy(8, 14))
    base_img.paste(img, position, img)
    return base_img


def run():
    i, j = 0, 0
    previous_trainer = None

    df = read_cube()

    base_img, output_path = get_deck_base_img(), get_deck_output_path()
    for row_number, stats in df.iterrows():
        pokemon_card_path = CARDS_OUTPUT_DIR / f'{row_number}_{stats.pokedex_name}.png'
        if i == 70 or is_trainer_deck_boundary(previous_trainer, stats):
            i = 0
            j += 1
            base_img.save(output_path)
            base_img, output_path = get_deck_base_img(), get_deck_output_path(j)

        base_img = add_card_at_pos(base_img, pokemon_card_path, pos(i % 10, (i // 10) % 7))

        i += 1
        previous_trainer = stats.trainer
    else:
        base_img.save(output_path)
