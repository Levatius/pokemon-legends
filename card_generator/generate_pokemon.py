from io import BytesIO

import pandas as pd
import requests
from PIL import ImageDraw
from tqdm import tqdm

from config import *
from utils import xy, read_cube, get_img, text_font, title_font, wrapped_text


#
# Base
#


def compose_base(stats):
    card_base = 'dark' if stats.encounter_tier in DARK_BASE_ENCOUNTER_TIERS else 'standard'
    base_img = get_img(CARD_ASSETS_DIR / 'card_bases' / f'{card_base}.png', xy(16, 28))

    if not pd.isnull(stats.climate):
        climate_name = stats.climate.lower()
    else:
        climate_name = 'unknown'

    climate_img = get_img(CARD_ASSETS_DIR / 'climates' / f'{climate_name}.png', xy(15.5, 27.5))
    base_img.paste(climate_img, xy(0.25, 0.25), climate_img)

    if not pd.isnull(stats.biome):
        biome_name = stats.biome.lower()
        biome_img = get_img(CARD_ASSETS_DIR / 'biomes' / f'{biome_name}.png', xy(15.5, 27.5))
        base_img.alpha_composite(biome_img, xy(0.25, 0.25))

    return base_img


def add_frame(img):
    frame_img = get_img(CARD_ASSETS_DIR / 'frame_base.png', xy(15.5, 19.25))
    img.paste(frame_img, xy(0.25, 0.25), frame_img)


#
# Pictures
#

def get_pokemon_img_size(stats):
    min_size = 7
    max_size = 11
    if not pd.isnull(stats.trainer):
        max_size = 10
    return max(min(stats.total // 2 + 3, max_size), min_size)


def converted_pokedex_number(stats):
    split_pokedex_number = str(stats.pokedex_number).split('-')
    if split_pokedex_number[0].isdigit():
        split_pokedex_number[0] = f'{int(split_pokedex_number[0]):03}'
    return '-'.join(split_pokedex_number)


def get_pokemon_img(stats):
    img_size = get_pokemon_img_size(stats)
    img_name = converted_pokedex_number(stats)
    try:
        pokemon_img = get_img(CARD_ASSETS_DIR / 'pokemon' / f'{img_name}.png', xy(img_size, img_size))
    except (FileNotFoundError, AttributeError):
        response = requests.get(f'{ART_FORM_URL}/{img_name}.png')
        pokemon_img = get_img(BytesIO(response.content), xy(img_size, img_size))
        pokemon_img.save(CARD_ASSETS_DIR / 'pokemon' / f'{img_name}.png')
    return pokemon_img


def add_pokemon_img(img, stats):
    pokemon_img = get_pokemon_img(stats)
    pokemon_img_pos = xy((16 - pokemon_img.width / 64) / 2, (20 - pokemon_img.height / 64) / 2)
    img.paste(pokemon_img, pokemon_img_pos, pokemon_img)


def add_trainer(img, stats):
    # Do not add a trainer for a wild Pokémon
    if pd.isnull(stats.trainer):
        return

    trainer_img = get_img(CARD_ASSETS_DIR / 'trainers' / f'{stats.trainer}.png', xy(5, 9.5))
    img.paste(trainer_img, xy(0, 6.75), trainer_img)

    rank_img = get_img(CARD_ASSETS_DIR / 'trainer_icons' / f'rank_{stats.encounter_tier}.png', xy(2.5, 2.5))
    img.paste(rank_img, xy(0.75, 16.75), rank_img)

    battle_img = get_img(CARD_ASSETS_DIR / 'trainer_icons' / f'battle.png', xy(2, 2))
    img.paste(battle_img, xy(13, 17), battle_img)


#
# Bases
#

def add_all_bases(img, stats):
    add_held_item_base(img, stats)
    add_location_base(img, stats)
    add_stats_bases(img)


def add_held_item_base(img, stats):
    # Do not add a held item base for a trainer Pokémon
    if not pd.isnull(stats.trainer):
        return

    if stats.uncapturable:
        img_name = 'uncapturable'
    else:
        for item_name, valid_descriptions in SPECIFIC_HELD_ITEM_BASE_LOOKUP.items():
            if stats.description in valid_descriptions:
                img_name = item_name
                break
        else:
            img_name = 'standard'

    held_item_base_img = get_img(CARD_ASSETS_DIR / 'held_item_bases' / f'{img_name}.png', xy(3.5, 3.5))
    img.paste(held_item_base_img, xy(1.75, 12.75), held_item_base_img)


def add_location_base(img, stats):
    # Do not add a location base for a trainer Pokémon
    if not pd.isnull(stats.trainer):
        return

    if stats.encounter_tier in ('ultra_beast', 'ultra_burst'):
        prism_armour_base_img = get_img(CARD_ASSETS_DIR / 'location_bases' / 'prism_armour.png', xy(3.5, 4))
        img.paste(prism_armour_base_img, xy(10.75, 12.5), prism_armour_base_img)
    else:
        location_base_img = get_img(CARD_ASSETS_DIR / 'location_bases' / 'standard.png', xy(3.5, 3.5))
        img.paste(location_base_img, xy(10.75, 12.75), location_base_img)


def add_stats_bases(img):
    health_base_img = get_img(CARD_ASSETS_DIR / 'stats_bases' / 'health.png', xy(3.5, 2))
    img.paste(health_base_img, xy(11.75, 7.75), health_base_img)
    initiative_base_img = get_img(CARD_ASSETS_DIR / 'stats_bases' / 'initiative.png', xy(3.5, 2))
    img.paste(initiative_base_img, xy(11.75, 10.25), initiative_base_img)


#
# Icons
#

def add_all_icons(img, stats):
    add_type_icons(img, stats)
    add_learnable_type_icons(img, stats)
    add_encounter_icon(img, stats)
    add_location_icon(img, stats)
    add_evolution_icon(img, stats)


def get_types(stats):
    return [type_ for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]


def add_type_icons(img, stats):
    types = get_types(stats)
    for i, type_ in enumerate(types):
        type_img = get_img(CARD_ASSETS_DIR / 'types' / f'{type_}.png', xy(2.5, 2.5))
        type_pos = xy(0.5 + i * 2.5, 0.5)
        img.paste(type_img, type_pos, type_img)


def get_learnable_types(stats):
    return [move for move in (stats.move_1, stats.move_2, stats.move_3, stats.move_4) if not pd.isnull(move)]


def add_learnable_type_icons(img, stats):
    # Do not add learnable types for a trainer Pokémon
    if not pd.isnull(stats.trainer):
        return

    learnable_types = get_learnable_types(stats)
    for i, type_ in enumerate(learnable_types):
        type_size = 1.25
        type_img = get_img(CARD_ASSETS_DIR / 'types' / f'{type_}.png', xy(type_size, type_size))
        type_pos = xy(3.25 - (len(learnable_types) / 2 * type_size) + (i % 2 * type_size), 16.75 + i // 2 * type_size)
        img.paste(type_img, type_pos, type_img)


def add_encounter_icon(img, stats):
    if stats.encounter_tier in GALACTIC_ENCOUNTER_TIERS:
        encounter_icon_name = 'galactic'
    else:
        encounter_icon_name = stats.encounter_tier

    encounter_icon_img = get_img(CARD_ASSETS_DIR / 'encounter_icons' / f'{encounter_icon_name}.png', xy(2, 2))
    img.paste(encounter_icon_img, xy(7, 17), encounter_icon_img)


def add_location_icon(img, stats):
    # Do not add a location for a trainer Pokémon
    if not pd.isnull(stats.trainer):
        return

    if stats.encounter_tier not in ('ultra_beast', 'ultra_burst'):
        try:
            location_icon_name = f'{stats.climate.lower()}_{stats.biome.lower()}'
            location_icon_img = get_img(CARD_ASSETS_DIR / 'location_icons' / f'{location_icon_name}.png', xy(3, 3))
        except (FileNotFoundError, AttributeError):
            location_icon_img = get_img(CARD_ASSETS_DIR / 'location_icons' / f'unknown.png', xy(3, 3))

        img.paste(location_icon_img, xy(11, 13), location_icon_img)


def add_evolution_icon(img, stats):
    # Do not add evolution cost for a trainer Pokémon
    if not pd.isnull(stats.trainer):
        return

    if not pd.isnull(stats.evolve_into):
        evolution_icon_name = 'standard'
    else:
        evolution_icon_name = 'final'

    evolution_icon_img = get_img(CARD_ASSETS_DIR / 'evolution_icons' / f'{evolution_icon_name}.png', xy(2.5, 2.5))
    img.paste(evolution_icon_img, xy(12.75, 16.75), evolution_icon_img)


#
# Finishing Touches
#


def add_text(img, stats):
    d = ImageDraw.Draw(img)
    types = get_types(stats)

    # Pokémon Name
    name_pos = xy(1 + len(types) * 2.5, 1.75 - (0.5 if not pd.isnull(stats.description) else 0))
    name_font_size = text_font(44) if pd.isnull(stats.description) else text_font(36)
    d.text(name_pos, stats.pokedex_name, fill=DARK_COLOUR, font=name_font_size, anchor='lm')

    # Pokémon Description
    if not pd.isnull(stats.description):
        d.text(xy(1 + len(types) * 2.5, 2.5), stats.description, fill=DARK_COLOUR, font=text_font(22), anchor='lm')

    # Pokémon Stats
    wrapped_text(d, str(int(stats.health)), title_font(44), boundaries=(1.5, 1.5), xy=xy(12.75, 8.75), fill=DARK_COLOUR,
                 anchor='mm')
    wrapped_text(d, str(int(stats.initiative)), title_font(44), boundaries=(1.5, 1.5), xy=xy(12.75, 11.25),
                 fill=DARK_COLOUR, anchor='mm')

    # Pokémon Evolution Cost
    if not pd.isnull(stats.evolve_cost):
        d.text(xy(14, 18), str(int(stats.evolve_cost)), fill=WHITE_COLOUR, font=title_font(44), anchor='mm')


def add_move(img, stats):
    move_img = get_img(MOVES_OUTPUT_DIR / f'{stats.move_name}.png', xy(14.5, 7.5))
    img.paste(move_img, xy(0.75, 19.75), move_img)


def add_emblem(img):
    if VANILLA_EMBLEM_PATH.is_file():
        emblem_name = 'vanilla'
    else:
        emblem_name = 'custom'
    emblem_img = get_img(CARD_ASSETS_DIR / 'emblems' / f'{emblem_name}.png', xy(0.5, 0.5))
    img.paste(emblem_img, xy(15, 27), emblem_img)


#
# Entry
#


def run(overwrite=False):
    print('Generating card fronts:')
    CARD_FRONTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = read_cube()
    for i, stats in tqdm(df.iterrows(), total=df.shape[0]):
        output_path = CARD_FRONTS_OUTPUT_DIR / f'{i}_{stats.pokedex_name.lower()}.png'
        if output_path.is_file() and not overwrite:
            continue

        img = compose_base(stats)

        # img = Image.new('RGBA', xy(16, 28))
        add_frame(img)
        add_pokemon_img(img, stats)
        add_trainer(img, stats)

        add_all_bases(img, stats)

        add_all_icons(img, stats)

        add_text(img, stats)
        add_move(img, stats)
        add_emblem(img)

        # base_img.paste(img, xy(0, 0), img)
        img.save(output_path)


if __name__ == '__main__':
    run(overwrite=True)
