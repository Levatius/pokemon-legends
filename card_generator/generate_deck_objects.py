import json

import pandas as pd

from config import *
from utils import read_cube, is_trainer_deck_boundary


def get_deck_json(j=0, is_trainer_deck=False):
    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    deck_json['ObjectStates'][0]['ColorDiffuse'] = {'r': 37 / 255, 'g': 37 / 255,
                                                    'b': 50 / 255} if is_trainer_deck else {'r': 150 / 255,
                                                                                            'g': 75 / 255,
                                                                                            'b': 50 / 255}
    deck_json['ObjectStates'][0]['CustomDeck']['1']['FaceURL'] = DECK_FACE_CLOUD_URLS[j]
    deck_json['ObjectStates'][0]['CustomDeck']['1'][
        'BackURL'] = PERFECT_WORLD_ORDER_CARD_BACK_CLOUD_URL if is_trainer_deck else STANDARD_CARD_BACK_CLOUD_URL
    return deck_json


def get_description(stats):
    if pd.isnull(stats.trainer):
        return f'The {stats.classification}'
    else:
        return stats.description


def get_card_type(stats, is_evolution):
    if is_evolution:
        return 'Evolution Card'

    if pd.isnull(stats.trainer):
        if stats.is_legendary:
            return 'Legendary Encounter Card'
        elif stats.power >= 7:
            return 'Strong Encounter Card'
        elif stats.power >= 5:
            return 'Moderate Encounter Card'
        elif stats.power >= 1:
            return 'Weak Encounter Card'
    else:
        return 'Perfect World Order Card'


def get_tags(stats, is_evolution=False):
    return [
        tag for tag in
        [
            "Pokemon Card",
            stats.biome,
            stats.climate,
            get_card_type(stats, is_evolution)
        ]
        if not pd.isnull(tag)
    ]


def get_lua_table_from_fields(fields):
    values_list = [f'"{value.capitalize()}"' for value in fields if not pd.isnull(value)]
    values_str = ','.join(values_list)
    return '{' + values_str + '}'


def get_lua_table_from_field(field):
    if not pd.isnull(field):
        values_list = [f'"{value}"' for value in field.split('/')]
        values_str = ','.join(values_list)
        return '{' + values_str + '}'
    return 'nil'


def get_lua_script(stats):
    local_variables = {
        'pokedex_name': f'"{stats.pokedex_name}"',
        'internal_name': f'"{stats.internal_name}"',
        'power': stats.power,
        'types': get_lua_table_from_fields((stats.type_1, stats.type_2)),
        'moves': get_lua_table_from_fields((stats.move_1, stats.move_2, stats.move_3)),
        'evolve_into': get_lua_table_from_field(stats.evolve_into),
        'evolve_apricorn': get_lua_table_from_field(stats.evolve_apricorn),
        'evolve_cost': int(stats.evolve_cost) if not pd.isnull(stats.evolve_into) else 'nil'
    }
    lua_script_lines = [f'{variable} = {value}' for variable, value in local_variables.items()]
    return '\n'.join(lua_script_lines)


def get_card_json(i, j, stats, is_evolution=False):
    with open(CARD_OBJECT_TEMPLATE) as f:
        card_json = json.load(f)

    card_json['CardID'] = 100 + i
    card_json['Nickname'] = stats.internal_name
    card_json['Description'] = get_description(stats)
    card_json['Tags'] = get_tags(stats, is_evolution)
    card_json['LuaScript'] = get_lua_script(stats)
    card_json['CustomDeck']['1']['FaceURL'] = DECK_FACE_CLOUD_URLS[j]
    card_json['CustomDeck']['1']['BackURL'] = STANDARD_CARD_BACK_CLOUD_URL

    return card_json


def add_card_to_deck(deck_json, i, j, stats, is_evolution=False):
    card_json = get_card_json(i, j, stats, is_evolution)
    deck_json['ObjectStates'][0]['DeckIDs'].append(100 + i)
    deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)


def get_deck_object_output_path(j=0):
    return CARD_DECKS_OUTPUT_DIR / f'{j}_deck.json'


def run():
    i, j = 0, 0
    previous_trainer = None

    df = read_cube()
    deck_json, output_path = get_deck_json(), get_deck_object_output_path()
    for _, stats in df.iterrows():
        if i == 70 or is_trainer_deck_boundary(previous_trainer, stats):
            i = 0
            j += 1
            with open(output_path, 'w') as f:
                json.dump(deck_json, f)
            deck_json, output_path = get_deck_json(j, not pd.isnull(stats.trainer)), get_deck_object_output_path(j)

        for k in range(stats.number_in_deck):
            add_card_to_deck(deck_json, i, j, stats, is_evolution=(k != 0))

        i += 1
        previous_trainer = stats.trainer
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)
