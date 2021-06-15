from io import BytesIO

import pandas as pd
import requests
from PIL import Image, ImageDraw

from config import *
from utils import xy, read_cube


def compose_base(stats):
    base_img = Image.open(ASSETS_DIR / f'card_base.png').convert('RGBA').resize(xy(16, 28))

    try:
        habitat_img_name = f'{stats.habitat_climate.lower()}_{stats.habitat_biome.lower()}.png'
        habitat_img = Image.open(ASSETS_DIR / 'habitats' / habitat_img_name)
    except (FileNotFoundError, AttributeError):
        habitat_img = Image.open(ASSETS_DIR / 'habitats' / 'unknown.png')

    habitat_img = habitat_img.convert('RGBA').resize(xy(15.5, 27.5))
    base_img.paste(habitat_img, xy(0.25, 0.25), habitat_img)
    return base_img


def add_frame(img):
    frame_img = Image.open(ASSETS_DIR / 'frame_base.png').convert('RGBA').resize(xy(16, 28))
    img.paste(frame_img, xy(0, 0), frame_img)
    return frame_img


def add_types(img, stats):
    types = [type_ for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]

    for i, type_ in enumerate(types):
        type_img = Image.open(ASSETS_DIR / 'types' / f'{type_}.png').convert('RGBA').resize(xy(2, 2))
        img.paste(type_img, xy(0.75 + i * 2, 0.75), type_img)

    return img


# def add_evolve_base(img):
#     evolve_base_img = Image.open(ASSETS_DIR / f'evolve_icon.png').convert('RGBA').resize(xy(3, 3))
#     img.paste(evolve_base_img, xy(12.5, 6.5), evolve_base_img)
#     return img


def add_moves(img, stats):
    moves = [move for move in (stats.move_1, stats.move_2, stats.move_3) if not pd.isnull(move)]

    for i, move in enumerate(moves):
        move_img = Image.open(ASSETS_DIR / 'types' / f'{move}.png').convert('RGBA').resize(xy(2, 2))
        img.paste(move_img, xy(15.25 - (len(moves) * 2) + (i * 2), 25.25), move_img)

    return img


# def add_evolve_stats(img, stats):
#     d = ImageDraw.Draw(img)
#     d.text(xy(14, 8), str(int(stats.evolve_cost)), fill=WHITE_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
#     return img


def add_name_text(img, stats):
    types = [type_ for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]

    d = ImageDraw.Draw(img)
    d.text(xy(1.25 + len(types) * 2, 1.75 - (0.5 if not pd.isnull(stats.description) else 0)), stats.pokedex_name, fill=DARK_COLOUR, font=LARGE_TITLE_FONT, anchor='lm')
    if not pd.isnull(stats.description):
        d.text(xy(1.25 + len(types) * 2, 2.5), stats.description, fill=DARK_COLOUR, font=LARGE_BODY_FONT, anchor='lm')
    return img


def get_variant(stats):
    variant = ''
    if stats.pokedex_number in (422, 423) and stats.description == 'East Ocean Form':
        variant = '-e'
    elif stats.pokedex_number == 412:
        variant = '-p'
    elif stats.pokedex_number == 421:
        variant = '-s'
    return variant


def get_pokemon_art(stats):
    variant = get_variant(stats)
    response = requests.get(f'{ART_FORM_URL}/{stats.pokedex_number:03}{variant}.png')
    pokemon_art_size = max(stats.power + 4, 6)
    pokemon_art_img = Image.open(BytesIO(response.content)).convert('RGBA').resize(
        xy(pokemon_art_size, pokemon_art_size))
    return pokemon_art_img


def add_pokemon_art(img, stats):
    pokemon_art_img = get_pokemon_art(stats)
    img.paste(pokemon_art_img, xy((16 - pokemon_art_img.width / 64) / 2, (22 - pokemon_art_img.height / 64) / 2),
              pokemon_art_img)
    return img


def add_power_base(img):
    power_base_img = Image.open(ASSETS_DIR / 'power_base.png').convert('RGBA').resize(xy(3.5, 3.5))
    img.paste(power_base_img, xy(11.25, 14.25), power_base_img)
    return img

def add_legendary_icon(img, stats):
    if stats.is_legendary:
        legendary_icon_img = Image.open(ASSETS_DIR / 'legendary_icon.png').convert('RGBA').resize(xy(2, 2))
        img.paste(legendary_icon_img, xy(13.25, 0.75), legendary_icon_img)
    return img

def wrap_text(text, draw, font, max_width=13.5):
    text_list = text.split(' ')
    multiline_text_list = []
    for text in text_list:
        if not multiline_text_list or draw.textsize(f'{multiline_text_list[-1]} {text}', font)[0] >= 64 * max_width:
            multiline_text_list.append('')
        multiline_text_list[-1] += text + ' '
    return '\n'.join(multiline_text_list)


def add_text(img, stats):
    d = ImageDraw.Draw(img)
    d.text(xy(13, 16), str(stats.power), fill=DARK_COLOUR, font=POWER_FONT, anchor='mm')
    d.text(xy(8, 20), str(stats.ability_name), fill=DARK_COLOUR, font=SMALL_TITLE_FONT, anchor='mm')
    ability_description = wrap_text(str(stats.ability_description), d, LARGE_BODY_FONT)
    d.multiline_text(xy(8, 22.25), ability_description, fill=DARK_COLOUR, font=LARGE_BODY_FONT, anchor='mm', align='center')
    d.text(xy(3, 25.75), str(stats.habitat_climate), fill=DARK_COLOUR, font=LARGE_BODY_FONT, anchor='lm')
    d.text(xy(3, 26.75), str(stats.habitat_biome), fill=DARK_COLOUR, font=LARGE_BODY_FONT, anchor='lm')
    return img


# def add_stats(img, attack, defence):
#     d = ImageDraw.Draw(img)
#     d.text(xy(13.5, 22.5), str(attack), fill=DARK_COLOUR, font=HUGE_TEXT_FONT, anchor='mm')
#     d.text(xy(13.5, 25.0), str(defence), fill=DARK_COLOUR, font=HUGE_TEXT_FONT, anchor='mm')
#     return img


def run(overwrite=False):
    df = read_cube()
    for i, stats in df.iterrows():
        output_path = CARDS_OUTPUT_DIR / f'{i}_{stats.pokedex_name.lower()}.png'
        if output_path.is_file() and not overwrite:
            print(f'Card for "{stats.pokedex_name}" exists, skipping')
            continue

        base_img = compose_base(stats)
        img = Image.new('RGBA', xy(16, 28))
        img = add_frame(img)
        img = add_pokemon_art(img, stats)
        img = add_power_base(img)
        img = add_types(img, stats)
        img = add_moves(img, stats)
        img = add_legendary_icon(img, stats)
        img = add_name_text(img, stats)
        img = add_text(img, stats)

        base_img.paste(img, xy(0, 0), img)
        base_img.save(output_path)
