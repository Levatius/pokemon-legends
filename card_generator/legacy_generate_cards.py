from io import BytesIO

import pandas as pd
import requests
from PIL import Image, ImageDraw

from config import *
from utils import xy, read_cube, get_shiny_name


def compose_base(stats, shiny):
    base_img = Image.open(ASSETS_DIR / f'base_{get_shiny_name(shiny)}.png').convert('RGBA').resize(xy(16, 28))

    try:
        habitat_img_name = f'{stats.habitat_climate.lower()}_{stats.habitat_biome.lower()}.png'
        habitat_img = Image.open(ASSETS_DIR / 'habitats' / habitat_img_name)
    except (FileNotFoundError, AttributeError):
        habitat_img = Image.open(ASSETS_DIR / 'habitats' / 'unknown.png')

    habitat_img = habitat_img.convert('RGBA').resize(xy(15.5, 27.5))
    base_img.paste(habitat_img, xy(0.25, 0.25), habitat_img)
    return base_img


def add_frame(img):
    frame_img = Image.open(ASSETS_DIR / 'frame.png').convert('RGBA').resize(xy(16, 28))
    img.paste(frame_img, xy(0, 0), frame_img)
    return frame_img


def add_types(img, stats):
    types = [type_ for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]

    for i, type_ in enumerate(types):
        type_img = Image.open(ASSETS_DIR / 'types' / f'{type_}.png').convert('RGBA').resize(xy(2.5, 2.5))
        img.paste(type_img, xy(1.25, 2.5 * i + 1.75), type_img)

    return img


def add_moves_base(img, stats):
    moves = [move for move in (stats.move_1, stats.move_2, stats.move_3) if not pd.isnull(move)]
    moves_base_img = Image.open(ASSETS_DIR / f'moves_{len(moves)}_icon.png').convert('RGBA').resize(
        xy(7, 3))
    img.paste(moves_base_img, xy(4.5, 24.5), moves_base_img)
    return img


def add_evolve_base(img):
    evolve_base_img = Image.open(ASSETS_DIR / f'evolve_icon.png').convert('RGBA').resize(xy(3, 3))
    img.paste(evolve_base_img, xy(12.5, 6.5), evolve_base_img)
    return img


def add_moves(img, stats):
    moves = [move for move in (stats.move_1, stats.move_2, stats.move_3) if not pd.isnull(move)]
    base_img = Image.new('RGBA', xy(7, 3))

    for i, move in enumerate(moves):
        move_img = Image.open(ASSETS_DIR / 'types' / f'{move}.png').convert('RGBA').resize(xy(2, 2))
        base_img.paste(move_img, xy(2 * i + (3 - len(moves) + 0.5), 0.5), move_img)

    img.paste(base_img, xy(4.5, 24.5), base_img)
    return img


def add_evolve_stats(img, stats):
    d = ImageDraw.Draw(img)
    d.text(xy(14, 8), str(int(stats.evolve_cost)), fill=WHITE_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    return img


def add_name(img, stats):
    d = ImageDraw.Draw(img)
    d.text(xy(8, 22.25), stats.pokedex_name, fill=DARK_COLOUR, font=MEDIUM_TEXT_FONT, anchor='mm')
    if not pd.isnull(stats.description):
        d.text(xy(8, 23.5), stats.description, fill=DARK_COLOUR, font=SMALL_TEXT_FONT, anchor='mm')
    return img


def get_variant(pokedex_number, description=None):
    variant = ''
    if pokedex_number in (422, 423) and description == 'East Ocean Form':
        variant = '-e'
    elif pokedex_number == 412:
        variant = '-p'
    elif pokedex_number == 421:
        variant = '-s'
    return variant


def get_art_size(tier):
    return max(tier + 4, 6)


def add_art(img, stats):
    variant = get_variant(stats.pokedex_number, stats.description)
    response = requests.get(f'{ART_FORM_URL}/{stats.pokedex_number:03}{variant}.png')
    art_size = get_art_size(stats.tier)
    art_img = Image.open(BytesIO(response.content)).convert('RGBA').resize(xy(art_size, art_size))
    img.paste(art_img, xy((16 - art_size) / 2, (28 - art_size) / 2), art_img)
    return img


def add_tier_base(img):
    tier_icon_img = Image.open(ASSETS_DIR / 'tier_icon.png').convert('RGBA').resize(xy(4, 4))
    img.paste(tier_icon_img, xy(0.5, 17.5), tier_icon_img)
    return img


def add_tier(img, stats):
    d = ImageDraw.Draw(img)
    d.text(xy(2.5, 19.5), str(stats.tier), fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    return img


def add_stats(img, attack, defence):
    d = ImageDraw.Draw(img)
    d.text(xy(13.5, 22.5), str(attack), fill=DARK_COLOUR, font=HUGE_TEXT_FONT, anchor='mm')
    d.text(xy(13.5, 25.0), str(defence), fill=DARK_COLOUR, font=HUGE_TEXT_FONT, anchor='mm')
    return img


def add_foil(img):
    foil_img = Image.open(ASSETS_DIR / 'foil.png').convert('RGBA').resize(xy(16, 28))
    foil_img_mask = img.copy()
    foil_img_mask.paste(foil_img, xy(0, 0), foil_img_mask)
    img.alpha_composite(foil_img_mask, xy(0, 0))
    return img


def run(overwrite=False, shiny=False):
    df = read_cube()
    for i, stats in df.iterrows():
        output_path = CARDS_OUTPUT_DIR / get_shiny_name(shiny) / f'{i}_{stats.pokedex_name.lower()}.png'
        if output_path.is_file() and not overwrite:
            print(f'Card for "{stats.pokedex_name}" exists, skipping')
            continue

        base_img = compose_base(stats, shiny)
        img = Image.new('RGBA', xy(16, 28))
        img = add_frame(img)
        img = add_moves_base(img, stats)
        img = add_evolve_base(img) if not pd.isnull(stats.evolve_into) else img
        img = add_art(img, stats)
        img = add_tier_base(img)
        img = add_foil(img) if shiny else img
        img = add_types(img, stats)
        img = add_moves(img, stats)
        img = add_evolve_stats(img, stats) if not pd.isnull(stats.evolve_into) else img
        img = add_tier(img, stats)
        img = add_name(img, stats)
        img = add_stats(img, attack=stats.attack + (1 if shiny else 0), defence=stats.defence + (1 if shiny else 0))

        base_img.paste(img, xy(0, 0), img)
        base_img.save(output_path)
