import pandas as pd
from PIL import ImageDraw
from tqdm import tqdm

from config import *
from utils import xy, read_cube, get_img, wrapped_text, text_font, title_font


def get_base():
    return get_img(CARD_ASSETS_DIR / 'move_base.png', xy(14.5, 7.5))


def add_header(img, stats):
    d = ImageDraw.Draw(img)

    # Move Type
    type_img = get_img(CARD_ASSETS_DIR / 'types' / f'{stats.move_type}.png', xy(2, 2))
    img.paste(type_img, xy(0.25, 0.25), type_img)

    # Move Name
    wrapped_text(d, stats.move_name, text_font(36), boundaries=(9.5, 1.75), xy=xy(7.25, 1.25), fill=DARK_COLOUR,
                 anchor='mm', align='center')

    # Move Attack Strength
    d.text(xy(13.25, 1.25), str(stats.move_attack_strength), fill=DARK_COLOUR, font=title_font(44), anchor='mm')


def add_effect(img, stats):
    d = ImageDraw.Draw(img)

    if pd.isnull(stats.move_class):
        effect_boundaries = (13.5, 4.5)
        effect_xy = xy(7.25, 4.75)
    else:
        effect_boundaries = (13.5, 3)
        effect_xy = xy(7.25, 4)

    wrapped_text(d, stats.move_effect, text_font(28), boundaries=effect_boundaries, xy=effect_xy, fill=DARK_COLOUR,
                 anchor='mm', align='center')


def add_class(img, stats):
    if pd.isnull(stats.move_class):
        return

    class_img = get_img(CARD_ASSETS_DIR / 'move_classes' / f'{stats.move_class}.png', xy(14.5, 1.5))
    img.paste(class_img, xy(0, 6), class_img)


def generate_moves(overwrite):
    print('Generating moves:')
    MOVES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = read_cube(sheet_name='moves')
    for _, stats in tqdm(df.iterrows(), total=df.shape[0]):
        output_path = MOVES_OUTPUT_DIR / f'{stats.move_name}.png'
        if output_path.is_file() and not overwrite:
            continue

        img = get_base()
        add_header(img, stats)
        add_effect(img, stats)
        add_class(img, stats)
        img.save(output_path)


def generate_card_backs(overwrite):
    print('Generating card backs:')
    CARD_BACKS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = read_cube(sheet_name='moves')
    for _, stats in tqdm(df.iterrows(), total=df.shape[0]):
        output_path = CARD_BACKS_OUTPUT_DIR / f'{stats.move_name}.png'
        if output_path.is_file() and not overwrite:
            continue

        img = get_img(CARD_ASSETS_DIR / 'card_backs' / f'standard.png', xy(16, 28))
        move_img = get_img(MOVES_OUTPUT_DIR / f'{stats.move_name}.png', xy(14.5, 7.5))
        img.paste(move_img, xy(0.75, 19.75), move_img)
        img.save(output_path)


def run(overwrite=False):
    generate_moves(overwrite)
    generate_card_backs(overwrite)


if __name__ == '__main__':
    run(overwrite=False)
