import json
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests
from PIL import Image, ImageDraw, ImageFont

COMPONENT_DIR = Path(__file__).parent
ROOT_DIR = COMPONENT_DIR.parent
ASSETS_DIR = COMPONENT_DIR / 'assets'
OUTPUT_DIR = COMPONENT_DIR / 'output'
CARDS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_cards'
DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_decks'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

REGULAR_SPRITE_URL = 'https://www.serebii.net/blackwhite/pokemon'
ART_FORM_URL = 'https://www.serebii.net/pokemon/art'
LARGE_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=128)
MEDIUM_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=64)
SMALL_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=32)
DARK_COLOUR = (37, 37, 50)

NORMAL_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1805355726852280537/DE6D896DBB79A48536CF06DF3D87042FC2EAF92E/'
NORMAL_DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1805355726848796619/D8DAA36D39E2953F1385AF433A2B50E957E4492E/',
    'http://cloud-3.steamusercontent.com/ugc/1805355726848797309/DC06F5F74AED63A3B2F93E9B57C651D5668E7E67/',
    'http://cloud-3.steamusercontent.com/ugc/1805355726848799378/A1F3D09DE66E55BC2F6592006B836C94EA11C885/'
]
SHINY_CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1805355726852279751/41E3CB188BD5830484ACC477F5855BDA9E88A759/'
SHINY_DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1805355726852282557/0289B4FF700974A9FD46284E7C975D60FB9000B4/',
    'http://cloud-3.steamusercontent.com/ugc/1805355726852285417/BD456D2C93F8F3568C2D6F5D1C2342FA5E3480AD/',
    'http://cloud-3.steamusercontent.com/ugc/1805355726852287024/356B36FC86A930D75222254FEB1CE4FEC17CA9D4/'
]


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def pos(x, y):
    return int(512 * x), int(896 * y)


def read_cube(cube_name='sinnoh_cube', sheet_name='sinnoh'):
    df = pd.read_excel(ROOT_DIR / f'{cube_name}.xlsx', sheet_name)
    return df


def compose_base(stats, shiny):
    base_img = Image.open(ASSETS_DIR / f'base_{get_shiny_name(shiny)}.png').convert('RGBA').resize(xy(16, 28))

    habitat_img_name = f'{stats.habitat_climate.lower()}_{stats.habitat_biome.lower()}.png' if (
            not pd.isnull(stats.habitat_biome) and not pd.isnull(stats.habitat_climate)) else 'unknown.png'
    habitat_img = Image.open(ASSETS_DIR / 'habitats' / habitat_img_name).convert('RGBA').resize(xy(15.5, 27.5))
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


def add_moves(img, stats):
    moves = [move for move in (stats.move_1, stats.move_2, stats.move_3) if not pd.isnull(move)]
    base_img = Image.new('RGBA', xy(7, 3))

    for i, move in enumerate(moves):
        move_img = Image.open(ASSETS_DIR / 'types' / f'{move}.png').convert('RGBA').resize(xy(2, 2))
        base_img.paste(move_img, xy(2 * i + (3 - len(moves) + 0.5), 0.5), move_img)

    img.paste(base_img, xy(4.5, 24.5), base_img)
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
    d.text(xy(2.5, 19.5), str(stats.tier), fill=DARK_COLOUR, font=MEDIUM_TEXT_FONT, anchor='mm')
    return img


def add_stats(img, attack, defence):
    d = ImageDraw.Draw(img)
    d.text(xy(13.5, 22.5), str(attack), fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    d.text(xy(13.5, 25.0), str(defence), fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    return img


def add_foil(img):
    foil_img = Image.open(ASSETS_DIR / 'foil.png').convert('RGBA').resize(xy(16, 28))
    foil_img_mask = img.copy()
    foil_img_mask.paste(foil_img, xy(0, 0), foil_img_mask)
    img.alpha_composite(foil_img_mask, xy(0, 0))
    return img


def get_shiny_name(shiny):
    return 'shiny' if shiny else 'normal'


def generate_cards(overwrite=False, shiny=False):
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
        img = add_art(img, stats)
        img = add_tier_base(img)

        if shiny:
            img = add_foil(img)

        img = add_types(img, stats)
        img = add_moves(img, stats)
        img = add_tier(img, stats)
        img = add_name(img, stats)
        img = add_stats(img, attack=stats.attack + 1 if shiny else 0, defence=stats.defence + 1 if shiny else 0)

        base_img.paste(img, xy(0, 0), img)
        base_img.save(output_path)


def get_deck_base_img():
    return Image.new('RGBA', pos(10, 7))


def get_deck_output_path(shiny, j=0):
    return DECKS_OUTPUT_DIR / get_shiny_name(shiny) / f'{j}_deck.png'


def add_card_at_pos(base_img, pokemon_card_path, pos):
    img = Image.open(pokemon_card_path).convert('RGBA').resize(xy(8, 14))
    base_img.paste(img, pos, img)
    return base_img


def generate_decks(shiny=False):
    pokemon_card_paths = sorted((CARDS_OUTPUT_DIR / get_shiny_name(shiny)).glob('*'),
                                key=lambda k: int(k.name.split('_')[0]))

    base_img, output_path = get_deck_base_img(), get_deck_output_path(shiny)
    for i, pokemon_card_path in enumerate(pokemon_card_paths):
        j = i // 70
        if j > 0 and i % 70 == 0:
            base_img.save(output_path)
            base_img, output_path = get_deck_base_img(), get_deck_output_path(shiny, j)

        base_img = add_card_at_pos(base_img, pokemon_card_path, pos(i % 10, (i // 10) % 7))
    else:
        base_img.save(output_path)


def get_deck_json(j=0):
    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    deck_json['ObjectStates'][0]['CustomDeck']['1']['FaceURL'] = NORMAL_DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['1']['BackURL'] = NORMAL_CARD_BACK_CLOUD_URL
    deck_json['ObjectStates'][0]['CustomDeck']['2']['FaceURL'] = SHINY_DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['2']['BackURL'] = SHINY_CARD_BACK_CLOUD_URL
    return deck_json


def get_tier_tag(tier):
    if tier >= 9:
        return 'Tier Uber'
    elif tier >= 7:
        return 'Tier High'
    elif tier >= 5:
        return 'Tier Medium'
    return 'Tier Low'


def get_lua_script(stats, shiny):
    local_variables = {
        'attack': stats.attack + (1 if shiny else 0),
        'defence': stats.defence + (1 if shiny else 0),
        'dexname': f'"{stats.pokedex_name}"',
        'tier': stats.tier,
        'types': '{' + ', '.join(
            [f'"{type_.capitalize()}"' for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]) + '}',
        'moves': '{' + ', '.join(
            [f'"{move.capitalize()}"' for move in (stats.move_1, stats.move_2, stats.move_3) if
             not pd.isnull(move)]) + '}',
        'form': f'"{get_shiny_name(shiny).capitalize()}"'
    }
    lua_script_lines = [f'{variable} = {value}' for variable, value in local_variables.items()]
    return '\n'.join(lua_script_lines)


def get_card_json(i, j, stats):
    with open(CARD_OBJECT_TEMPLATE) as f:
        card_json = json.load(f)

    shiny = False
    for subcard_json in (card_json, card_json['States']['2']):
        subcard_json['CardID'] = 100 + i % 70 if not shiny else 200 + i % 70
        subcard_json['Nickname'] = stats.pokedex_name + (' ★' if shiny else '')
        subcard_json['Description'] = f'The {stats.classification}'
        subcard_json['Tags'].extend([stats.habitat_biome, stats.habitat_climate, get_tier_tag(stats.tier)])
        subcard_json['LuaScript'] = get_lua_script(stats, shiny)
        subcard_json['CustomDeck']['1' if not shiny else '2']['FaceURL'] = NORMAL_DECK_FACE_CLOUD_URLS[
            j] if not shiny else SHINY_DECK_FACE_CLOUD_URLS[j]
        subcard_json['CustomDeck']['1' if not shiny else '2'][
            'BackURL'] = NORMAL_CARD_BACK_CLOUD_URL if not shiny else SHINY_CARD_BACK_CLOUD_URL
        shiny = True

    return card_json


def add_card_to_deck(deck_json, i, j, stats):
    card_json = get_card_json(i, j, stats)
    deck_json['ObjectStates'][0]['DeckIDs'].append(100 + i % 70)
    deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)


def get_deck_object_output_path(j=0):
    return DECKS_OUTPUT_DIR / f'{j}_deck.json'


def generate_deck_objects():
    df = read_cube()
    deck_json, output_path = get_deck_json(), get_deck_object_output_path()
    for i, stats in df.iterrows():
        j = i // 70
        if j > 0 and i % 70 == 0:
            with open(output_path, 'w') as f:
                json.dump(deck_json, f)
            deck_json, output_path = get_deck_json(j), get_deck_object_output_path(j)

        add_card_to_deck(deck_json, i, j, stats)
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)


if __name__ == '__main__':
    # generate_cards(overwrite=True)
    # generate_decks()
    generate_cards(overwrite=True, shiny=True)
    generate_decks(shiny=True)
    # generate_deck_objects()
