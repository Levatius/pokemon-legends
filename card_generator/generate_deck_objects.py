import json

import pandas as pd

from config import *
from utils import read_cube, get_shiny_name


def get_deck_json(j=0):
    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    deck_json['ObjectStates'][0]['CustomDeck']['1']['FaceURL'] = NORMAL_DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['1']['BackURL'] = NORMAL_CARD_BACK_CLOUD_URL
    deck_json['ObjectStates'][0]['CustomDeck']['2']['FaceURL'] = SHINY_DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['2']['BackURL'] = SHINY_CARD_BACK_CLOUD_URL
    return deck_json


def get_tier_tag(tier):
    if isinstance(tier, str):
        return None
    if tier >= 9:
        return 'Tier Uber'
    elif tier >= 7:
        return 'Tier High'
    elif tier >= 5:
        return 'Tier Medium'
    return 'Tier Low'


def get_evolution_tag(is_evolution):
    if is_evolution:
        return 'Evolution Card'
    return None


def get_legendary_tag(is_legendary):
    if is_legendary:
        return 'Legendary'
    return None


def get_tags(stats, is_evolution=False):
    return [
        tag for tag in
        [
            stats.habitat_biome,
            stats.habitat_climate,
            get_tier_tag(stats.tier),
            get_evolution_tag(is_evolution),
            get_legendary_tag(stats.is_legendary)
        ]
        if not pd.isnull(tag)
    ]


def get_lua_table_from_fields(fields):
    values_list = [f'"{value.capitalize()}"' for value in fields if not pd.isnull(value)]
    values_str = ','.join(values_list)
    return '{' + values_str + '}'


def get_lua_table_from_field(field):
    if not pd.isnull(field):
        values_list = [f'"{value}"' for value in field.split(',')]
        values_str = ','.join(values_list)
        return '{' + values_str + '}'
    return 'nil'


def get_lua_script(stats, shiny):
    local_variables = {
        'pokedex_name': f'"{stats.pokedex_name}"',
        'internal_name': f'"{stats.internal_name}"',
        'attack': stats.attack + (1 if shiny else 0),
        'defence': stats.defence + (1 if shiny else 0),
        'tier': stats.tier,
        'types': get_lua_table_from_fields((stats.type_1, stats.type_2)),
        'moves': get_lua_table_from_fields((stats.move_1, stats.move_2, stats.move_3)),
        'form': f'"{get_shiny_name(shiny).capitalize()}"',
        'evolve_into': get_lua_table_from_field(stats.evolve_into),
        'evolve_apricorn': get_lua_table_from_field(stats.evolve_apricorn),
        'evolve_cost': int(stats.evolve_cost) if not pd.isnull(stats.evolve_into) else 'nil'
        # 'evolve_lake_requirement': stats.evolve_lake_requirement if not pd.isnull(stats.evolve_into) else 'nil'
    }
    lua_script_lines = [f'{variable} = {value}' for variable, value in local_variables.items()]
    return '\n'.join(lua_script_lines)


def get_card_json(i, j, stats, is_evolution=False):
    with open(CARD_OBJECT_TEMPLATE) as f:
        card_json = json.load(f)

    shiny = False
    for subcard_json in (card_json, card_json['States']['2']):
        subcard_json['CardID'] = 100 + i % 70 if not shiny else 200 + i % 70
        subcard_json['Nickname'] = stats.internal_name + (' ★' if shiny else '')
        subcard_json['Description'] = f'The {stats.classification}'
        subcard_json['Tags'].extend(get_tags(stats, is_evolution))
        subcard_json['LuaScript'] = get_lua_script(stats, shiny)
        subcard_json['CustomDeck']['1' if not shiny else '2']['FaceURL'] = NORMAL_DECK_FACE_CLOUD_URLS[
            j] if not shiny else SHINY_DECK_FACE_CLOUD_URLS[j]
        subcard_json['CustomDeck']['1' if not shiny else '2'][
            'BackURL'] = NORMAL_CARD_BACK_CLOUD_URL if not shiny else SHINY_CARD_BACK_CLOUD_URL
        shiny = True

    return card_json


def add_card_to_deck(deck_json, i, j, stats, is_evolution=False):
    card_json = get_card_json(i, j, stats, is_evolution)
    deck_json['ObjectStates'][0]['DeckIDs'].append(100 + i % 70)
    deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)


def get_deck_object_output_path(j=0):
    return DECKS_OUTPUT_DIR / f'{j}_deck.json'


def run():
    df = read_cube()
    deck_json, output_path = get_deck_json(), get_deck_object_output_path()
    for i, stats in df.iterrows():
        j = i // 70
        if j > 0 and i % 70 == 0:
            with open(output_path, 'w') as f:
                json.dump(deck_json, f)
            deck_json, output_path = get_deck_json(j), get_deck_object_output_path(j)

        for k in range(stats.number_in_deck):
            add_card_to_deck(deck_json, i, j, stats, is_evolution=(k != 0))
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)
