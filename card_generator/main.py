from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR / 'assets'
OUTPUT_DIR = COMPONENT_DIR / 'output'

SEREBII_URL = 'https://www.serebii.net/blackwhite/pokemon'
LARGE_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=64)
SMALL_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=32)
DARK_COLOUR = (37, 37, 50)


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def read_cube(cube_name='sinnoh_cube', sheet_name='sinnoh'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def compose_base(habitat_biome, habitat_climate):
    base_img = Image.open(ASSETS_DIR / 'base.png').convert('RGBA').resize(xy(16, 28))
    habitat_img_name = f'{habitat_climate.lower()}_{habitat_biome.lower()}.png' if (
            not pd.isnull(habitat_biome) and not pd.isnull(habitat_climate)) else 'unknown.png'
    habitat_img = Image.open(ASSETS_DIR / 'habitats' / habitat_img_name).convert('RGBA').resize(xy(15.5, 27.5))
    frame_img = Image.open(ASSETS_DIR / 'frame.png').convert('RGBA').resize(xy(16, 28))
    base_img.paste(habitat_img, xy(0.25, 0.25), habitat_img)
    base_img.paste(frame_img, xy(0, 0), frame_img)
    return base_img


def add_type(img, type_1, type_2=None):
    type_1_img = Image.open(ASSETS_DIR / 'types' / f'{type_1}.png').convert('RGBA').resize(xy(2.5, 2.5))
    img.paste(type_1_img, xy(1.25, 1.75), type_1_img)

    if not pd.isnull(type_2):
        type_2_img = Image.open(ASSETS_DIR / 'types' / f'{type_2}.png').convert('RGBA').resize(xy(2.5, 2.5))
        img.paste(type_2_img, xy(1.25, 4.25), type_2_img)
    return img


def add_name(img, name, description=None):
    d = ImageDraw.Draw(img)
    d.text(xy(8, 22.25), name, fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    if not pd.isnull(description):
        d.text(xy(8, 23.5), description, fill=DARK_COLOUR, font=SMALL_TEXT_FONT, anchor='mm')
    return img


def add_sprite(img, pokedex_number, description=None):
    variant = '-e' if description == 'East Ocean Form' else ''
    response = requests.get(f'{SEREBII_URL}/{pokedex_number:03}{variant}.png')
    sprite_img = Image.open(BytesIO(response.content)).convert('RGBA').resize(xy(13, 13))
    img.paste(sprite_img, xy(1.5, 7.5), sprite_img)
    return img


def add_tier(img, tier):
    tier_icon_img = Image.open(ASSETS_DIR / 'tier_icon.png').convert('RGBA').resize(xy(4, 4))
    img.paste(tier_icon_img, xy(0.5, 17.5), tier_icon_img)
    d = ImageDraw.Draw(img)
    d.text(xy(2.5, 19.5), str(tier), fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    return img


def run(overwrite=False):
    df = read_cube()
    for i, stats in df.iterrows():
        output_path = OUTPUT_DIR / f'{i}_{stats.pokedex_name.lower()}.png'
        if output_path.is_file() and not overwrite:
            print(f'Card for "{stats.pokedex_name}" exists, skipping')
            continue

        img = compose_base(habitat_biome=stats.habitat_biome, habitat_climate=stats.habitat_climate)
        img = add_type(img, type_1=stats.type_1, type_2=stats.type_2)
        img = add_name(img, name=stats.pokedex_name, description=stats.description)
        img = add_sprite(img, pokedex_number=stats.pokedex_number, description=stats.description)
        img = add_tier(img, tier=stats.tier)
        img.save(output_path)


if __name__ == '__main__':
    run(overwrite=False)
