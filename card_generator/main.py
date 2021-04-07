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
CARDS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_cards_art_form'
DECKS_OUTPUT_DIR = OUTPUT_DIR / 'pokemon_decks'
CARD_OBJECT_TEMPLATE = ASSETS_DIR / 'card_object_template.json'
DECK_OBJECT_TEMPLATE = ASSETS_DIR / 'deck_object_template.json'

REGULAR_SPRITE_URL = 'https://www.serebii.net/blackwhite/pokemon'
ART_FORM_URL = 'https://www.serebii.net/pokemon/art'
LARGE_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=64)
SMALL_TEXT_FONT = ImageFont.truetype(str(ASSETS_DIR / 'la_oriental.otf'), size=32)
DARK_COLOUR = (37, 37, 50)

CARD_BACK_CLOUD_URL = 'http://cloud-3.steamusercontent.com/ugc/1805355664340194820/DE6D896DBB79A48536CF06DF3D87042FC2EAF92E/'
DECK_FACE_CLOUD_URLS = [
    'http://cloud-3.steamusercontent.com/ugc/1805355704318290947/6545C4948069477870DD13F5C865C4A1CB831F3B/',
    'http://cloud-3.steamusercontent.com/ugc/1805355704318291398/FB25504EF94CD7BD8AADD035A26DE758DB2E8273/',
    'http://cloud-3.steamusercontent.com/ugc/1805355704318292085/BDCE9068A60CB8A3E379D90ED89663666932FCB1/'
]


def xy(width_cm, height_cm):
    return int(64 * width_cm), int(64 * height_cm)


def pos(x, y):
    return int(512 * x), int(896 * y)


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


def get_variant(pokedex_number, description=None, art_form=False):
    variant = ''
    if pokedex_number in (422, 423) and description == 'East Ocean Form':
        variant = '-e'
    elif pokedex_number == 412 and art_form:
        variant = '-p'
    return variant


def add_sprite(img, pokedex_number, description=None):
    variant = get_variant(pokedex_number, description)
    response = requests.get(f'{REGULAR_SPRITE_URL}/{pokedex_number:03}{variant}.png')
    sprite_img = Image.open(BytesIO(response.content)).convert('RGBA').resize(xy(13, 13))
    img.paste(sprite_img, xy(1, 7), sprite_img)
    return img


def get_art_size(tier):
    return max(tier + 4, 6)


def add_art(img, pokedex_number, tier, description=None):
    variant = get_variant(pokedex_number, description, art_form=True)
    response = requests.get(f'{ART_FORM_URL}/{pokedex_number:03}{variant}.png')
    art_size = get_art_size(tier)
    art_img = Image.open(BytesIO(response.content)).convert('RGBA').resize(xy(art_size, art_size))
    img.paste(art_img, xy((16 - art_size) / 2, (28 - art_size) / 2), art_img)
    return img


def add_tier(img, tier):
    tier_icon_img = Image.open(ASSETS_DIR / 'tier_icon.png').convert('RGBA').resize(xy(4, 4))
    img.paste(tier_icon_img, xy(0.5, 17.5), tier_icon_img)
    d = ImageDraw.Draw(img)
    d.text(xy(2.5, 19.5), str(tier), fill=DARK_COLOUR, font=LARGE_TEXT_FONT, anchor='mm')
    return img


def generate_cards(overwrite=False):
    df = read_cube()
    for i, stats in df.iterrows():
        output_path = CARDS_OUTPUT_DIR / f'{i}_{stats.pokedex_name.lower()}.png'
        if output_path.is_file() and not overwrite:
            print(f'Card for "{stats.pokedex_name}" exists, skipping')
            continue

        img = compose_base(habitat_biome=stats.habitat_biome, habitat_climate=stats.habitat_climate)
        img = add_type(img, type_1=stats.type_1, type_2=stats.type_2)
        img = add_name(img, name=stats.pokedex_name, description=stats.description)
        img = add_art(img, pokedex_number=stats.pokedex_number, tier=stats.tier, description=stats.description)
        img = add_tier(img, tier=stats.tier)
        img.save(output_path)


def get_base_img():
    return Image.new('RGBA', pos(10, 7))


def get_output_path(j=0, filetype='png'):
    return DECKS_OUTPUT_DIR / f'{j}_deck.{filetype}'


def add_card_at_pos(base_img, pokemon_card_path, pos):
    img = Image.open(pokemon_card_path).convert('RGBA').resize(xy(8, 14))
    base_img.paste(img, pos, img)
    return base_img


def generate_decks():
    pokemon_card_paths = sorted(CARDS_OUTPUT_DIR.glob('*'), key=lambda k: int(k.name.split('_')[0]))

    base_img, output_path = get_base_img(), get_output_path()
    for i, pokemon_card_path in enumerate(pokemon_card_paths):
        j = i // 70
        if j > 0 and i % 70 == 0:
            base_img.save(output_path)
            base_img, output_path = get_base_img(), get_output_path(j)

        base_img = add_card_at_pos(base_img, pokemon_card_path, pos(i % 10, (i // 10) % 7))
    else:
        base_img.save(output_path)


def get_deck_json(j=0):
    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    deck_json['ObjectStates'][0]['CustomDeck']['1']['FaceURL'] = DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['1']['BackURL'] = CARD_BACK_CLOUD_URL
    return deck_json


def get_tier_tag(tier):
    if tier >= 9:
        return 'Tier Uber'
    elif tier >= 7:
        return 'Tier High'
    elif tier >= 5:
        return 'Tier Medium'
    return 'Tier Low'


def get_lua_script(stats):
    local_variables = {
        'base_attack': stats.attack,
        'base_defence': stats.defence,
        'dexname': f'"{stats.pokedex_name}"',
        'tier': stats.tier,
        'types': '{' + ', '.join([f'"{type_.capitalize()}"' for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]) + '}',
        'moves': '{' + ', '.join([f'"{type_.capitalize()}"' for type_ in (stats.type_1, stats.type_2) if not pd.isnull(type_)]) + '}'
    }
    lua_script_lines = [f'local {variable} = {value}' for variable, value in local_variables.items()]
    lua_script_lines.append('\n#include pokemon-legends/tabletop_src/pokemon_card\n--EOF')
    return '\n'.join(lua_script_lines)


def get_card_json(stats):
    with open(CARD_OBJECT_TEMPLATE) as f:
        card_json = json.load(f)
    card_json['Nickname'] = stats.pokedex_name
    card_json['Description'] = f'The {stats.classification}'
    card_json['Tags'].extend([stats.habitat_biome, stats.habitat_climate, get_tier_tag(stats.tier)])
    card_json['LuaScript'] = get_lua_script(stats)
    return card_json


def add_card_to_deck(deck_json, i, stats):
    card_json = get_card_json(stats)
    deck_json['ObjectStates'][0]['DeckIDs'].append(100 + i % 70)
    deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)


def generate_deck_objects():
    df = read_cube()
    deck_json, output_path = get_deck_json(), get_output_path(filetype='json')
    for i, stats in df.iterrows():
        j = i // 70
        if j > 0 and i % 70 == 0:
            with open(output_path, 'w') as f:
                json.dump(deck_json, f)
            deck_json, output_path = get_deck_json(j), get_output_path(j, filetype='json')

        add_card_to_deck(deck_json, i, stats)
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)


if __name__ == '__main__':
    # generate_cards(overwrite=False)
    # generate_decks()
    generate_deck_objects()
