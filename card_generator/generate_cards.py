from io import BytesIO

import pandas as pd
import requests
from PIL import Image, ImageDraw

from config import *
from utils import xy, read_cube


# Utils

def get_img(file_path, size):
    return Image.open(file_path).convert('RGBA').resize(size)


def get_types(stats):
    return [type_ for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]


def get_moves(stats):
    return [move for move in (stats.move_1, stats.move_2, stats.move_3) if not pd.isnull(move)]


def wrap_text(text, draw, font, max_width):
    text_list = text.split(' ')
    multiline_text_list = []
    for text in text_list:
        if not multiline_text_list or draw.textsize(f'{multiline_text_list[-1]} {text}', font)[0] >= 64 * max_width:
            multiline_text_list.append('')
        multiline_text_list[-1] += text + ' '
    return '\n'.join(multiline_text_list)


# Functions


def compose_base(stats):
    card_base = 'standard' if pd.isnull(stats.trainer) else 'perfect_world_order'
    base_img = Image.open(ASSETS_DIR / 'card_bases' / f'{card_base}.png').convert('RGBA').resize(xy(16, 28))

    try:
        climate_img = Image.open(ASSETS_DIR / 'climates' / f'{stats.climate.lower()}.png')
    except (FileNotFoundError, AttributeError):
        climate_img = Image.open(ASSETS_DIR / 'climates' / f'unknown.png')

    climate_img = climate_img.convert('RGBA').resize(xy(15.5, 27.5))
    base_img.paste(climate_img, xy(0.25, 0.25), climate_img)

    try:
        biome_img = Image.open(ASSETS_DIR / 'biomes' / f'{stats.biome.lower()}.png')
        biome_img = biome_img.convert('RGBA').resize(xy(15.5, 27.5))
        base_img.alpha_composite(biome_img, xy(0.25, 0.25))
    except (FileNotFoundError, AttributeError):
        print(f'Biome {stats.biome} not recognised.')

    return base_img


def add_frame(img):
    frame_img = Image.open(ASSETS_DIR / 'frame_base.png').convert('RGBA').resize(xy(16, 28))
    img.paste(frame_img, xy(0, 0), frame_img)
    return frame_img


def add_types_and_moves(img, stats):
    types = get_types(stats)
    for i, type_ in enumerate(types):
        type_img = get_img(ASSETS_DIR / 'types' / f'{type_}.png', xy(2.5, 2.5))
        img.paste(type_img, xy(0.5 + i * 2.5, 0.5), type_img)

    moves = get_moves(stats)
    for i, move in enumerate(moves):
        move_img = get_img(ASSETS_DIR / 'types' / f'{move}.png', xy(2.5, 2.5))
        img.paste(move_img, xy(15.5 - (len(moves) * 2.5) + (i * 2.5), 25), move_img)

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


def get_size(stats):
    if not pd.isnull(stats.trainer):
        if stats.pokedex_number in (480, 481, 482, 474):
            return 7
    return max(min(stats.power + 4, 14), 6)


def get_pokemon_art(stats):
    variant = get_variant(stats)
    pokemon_art_size = get_size(stats)
    try:
        pokemon_art_img = get_img(ASSETS_DIR / 'pokemon' / f'{stats.pokedex_number:03}{variant}.png',
                                  xy(pokemon_art_size, pokemon_art_size))
    except (FileNotFoundError, AttributeError):
        response = requests.get(f'{ART_FORM_URL}/{stats.pokedex_number:03}{variant}.png')
        pokemon_art_img = get_img(BytesIO(response.content), xy(pokemon_art_size, pokemon_art_size))

    return pokemon_art_img


def add_pokemon_art(img, stats):
    pokemon_art_img = get_pokemon_art(stats)
    img.paste(pokemon_art_img, xy((16 - pokemon_art_img.width / 64) / 2, (20 - pokemon_art_img.height / 64) / 2),
              pokemon_art_img)
    return img


def add_bases(img):
    power_base_img = Image.open(ASSETS_DIR / 'power_base.png').convert('RGBA').resize(xy(3.5, 3.5))
    img.paste(power_base_img, xy(10.75, 12.75), power_base_img)
    ability_base_img = Image.open(ASSETS_DIR / 'ability_base.png').convert('RGBA').resize(xy(14.5, 7.5))
    img.paste(ability_base_img, xy(0.75, 16.75), ability_base_img)
    return img


def add_legendary_icon(img, stats):
    if stats.is_legendary:
        legendary_icon_img = Image.open(ASSETS_DIR / 'legendary_icon.png').convert('RGBA').resize(xy(2, 2))
        img.paste(legendary_icon_img, xy(13.25, 0.75), legendary_icon_img)
    return img


def add_trainer(img, stats):
    if not pd.isnull(stats.trainer):
        trainer_img = get_img(ASSETS_DIR / 'trainers' / f'{stats.trainer}.png', xy(5, 9.5))
        img.paste(trainer_img, xy(0, 6.75), trainer_img)
        trainer_icon_img = get_img(ASSETS_DIR / 'perfect_world_order_icon.png', xy(2, 2))
        img.paste(trainer_icon_img, xy(0.75, 25.25), trainer_icon_img)
    return img


def add_location(img, stats):
    if not pd.isnull(stats.trainer):
        return img

    d = ImageDraw.Draw(img)
    try:
        location_icon_img = get_img(ASSETS_DIR / 'map_icons' / f'{stats.climate.lower()}_{stats.biome.lower()}.png',
                                    xy(2.5, 2.5))
        climate_name = str(stats.climate)
        biome_name = str(stats.biome)
    except (FileNotFoundError, AttributeError):
        location_icon_img = get_img(ASSETS_DIR / 'map_icons' / f'unknown.png', xy(2.5, 2.5))
        climate_name = 'Location'
        biome_name = 'Unknown'

    img.paste(location_icon_img, xy(0.5, 25), location_icon_img)
    d.text(xy(3.25, 25.75), climate_name, fill=DARK_COLOUR, font=BARLOW_48, anchor='lm')
    d.text(xy(3.25, 26.75), biome_name, fill=DARK_COLOUR, font=BARLOW_48, anchor='lm')
    return img


def add_text(img, stats):
    d = ImageDraw.Draw(img)
    types = get_types(stats)

    d.text(
        xy(0.75 + len(types) * 2.5, 1.75 - (0.5 if not pd.isnull(stats.description) else 0)),
        stats.pokedex_name,
        fill=DARK_COLOUR,
        font=BARLOW_80,
        anchor='lm'
    )
    if not pd.isnull(stats.description):
        d.text(
            xy(0.75 + len(types) * 2.5, 2.5),
            stats.description,
            fill=DARK_COLOUR,
            font=BARLOW_48,
            anchor='lm'
        )
    d.text(xy(12.5, 14.5), str(stats.power), fill=DARK_COLOUR, font=ORIENTAL_160, anchor='mm')
    d.text(xy(8, 18), str(stats.ability_name), fill=DARK_COLOUR, font=BARLOW_80, anchor='mm')
    ability = wrap_text(str(stats.ability_description), d, BARLOW_64, max_width=13.5)
    d.multiline_text(xy(8, 21.5), ability, fill=DARK_COLOUR, font=BARLOW_64, anchor='mm', align='center')
    return img


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

        img = add_trainer(img, stats)
        img = add_pokemon_art(img, stats)
        img = add_bases(img)
        img = add_types_and_moves(img, stats)
        img = add_legendary_icon(img, stats)
        img = add_location(img, stats)
        img = add_text(img, stats)

        base_img.paste(img, xy(0, 0), img)
        base_img.save(output_path)
