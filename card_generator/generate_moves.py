import pandas as pd
from PIL import ImageDraw
from tqdm import tqdm

from config import *
from utils import xy, read_cube, get_img, wrap_text


def get_base():
    return get_img(ASSETS_DIR / 'move_base.png', xy(14.5, 7.5))


def add_header(img, stats):
    d = ImageDraw.Draw(img)

    type_img = get_img(ASSETS_DIR / 'types' / f'{stats.type}.png', xy(2, 2))
    img.paste(type_img, xy(0.25, 0.25), type_img)

    font = BARLOW_80
    if len(stats.move_name) > 16:
        font = BARLOW_64
    d.text(xy(7.25, 1.25), stats.move_name, fill=DARK_COLOUR, font=font, anchor='mm')
    if not pd.isnull(stats.damage):
        d.text(xy(13.25, 1.25), str(stats.damage), fill=DARK_COLOUR, font=ORIENTAL_96, anchor='mm')


def add_description(img, stats):
    if pd.isnull(stats.description):
        return
    d = ImageDraw.Draw(img)

    description = wrap_text(str(stats.description), d, BARLOW_64, max_width=13.5)
    d.multiline_text(xy(7.25, 4.75), description, fill=DARK_COLOUR, font=BARLOW_64, anchor='mm', align='center')


def add_effectiveness(img, stats):
    if stats.type not in TYPE_CHART:
        return

    d = ImageDraw.Draw(img)

    offset = 14.5
    for effectiveness, types in TYPE_CHART[stats.type].items():
        if not types:
            continue
        offset -= 0.5 + len(types) * 1
    offset = offset / 2

    for effectiveness, types in TYPE_CHART[stats.type].items():
        if not types:
            continue
        new_offset = offset + 0.5 + len(types) * 1
        d.rectangle((xy(offset, 7.25), xy(new_offset, 7.5)), fill=EFFECTIVENESS_COLOURS[effectiveness])
        for i, type_ in enumerate(types):
            type_img = get_img(ASSETS_DIR / 'types' / f'{type_}.png', xy(1, 1))
            img.paste(type_img, xy(offset + 0.25 + i * 1, 6.25), type_img)
        offset = new_offset


def run(overwrite=False):
    print('Generating moves:')
    MOVES_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = read_cube(sheet_name='moves')
    for _, stats in tqdm(df.iterrows(), total=df.shape[0]):
        output_path = MOVES_OUTPUT_DIR / f'{stats.move_name}.png'
        if output_path.is_file() and not overwrite:
            continue

        img = get_base()
        add_header(img, stats)
        add_description(img, stats)
        # add_effectiveness(img, stats)
        img.save(output_path)

    print('Generating card backs:')
    CARD_BACKS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for _, stats in tqdm(df.iterrows(), total=df.shape[0]):
        output_path = CARD_BACKS_OUTPUT_DIR / f'{stats.move_name}.png'
        if output_path.is_file() and not overwrite:
            continue

        img = get_img(ASSETS_DIR / 'card_backs' / f'standard.png', xy(16, 28))
        move_img = get_img(MOVES_OUTPUT_DIR / f'{stats.move_name}.png', xy(14.5, 7.5))
        img.paste(move_img, xy(0.75, 19.75), move_img)
        img.save(output_path)


if __name__ == '__main__':
    run(overwrite=True)
