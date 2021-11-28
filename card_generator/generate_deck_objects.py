import json

import pandas as pd
from tqdm import tqdm

from config import *
from utils import read_cube

DECK_OBJECTS = '{j}_deck.json'


def get_deck_json(j=0):
    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    deck_json['ObjectStates'][0]['ColorDiffuse'] = {'r': 150 / 255, 'g': 75 / 255, 'b': 50 / 255}
    deck_json['ObjectStates'][0]['CustomDeck']['1']['FaceURL'] = input(f'Enter cloud url for {CARD_FRONTS_DECK_IMG.format(j=j)}:\n')
    deck_json['ObjectStates'][0]['CustomDeck']['1']['BackURL'] = input(f'Enter cloud url for {CARD_BACKS_DECK_IMG.format(j=j)}:\n')
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
        encounter_tier_tag_map = {
            'starter': 'Starter Card',
            'weak': 'Weak Encounter Card',
            'moderate': 'Moderate Encounter Card',
            'strong': 'Strong Encounter Card',
            'legendary': 'Legendary Encounter Card'
        }
        return encounter_tier_tag_map.get(stats.encounter_tier)


def get_encounter_tier_tag(stats, is_evolution):
    if is_evolution:
        return 'Evolution Card'

    if pd.isnull(stats.trainer):
        encounter_tier_tag_map = {
            'starter': 'Starter Card',
            'weak': 'Weak Encounter Card',
            'moderate': 'Moderate Encounter Card',
            'strong': 'Strong Encounter Card',
            'legendary': 'Legendary Encounter Card'
        }
        return encounter_tier_tag_map.get(stats.encounter_tier)
    else:
        trainer_tier_tag_map = {
            'grunt': 'Galactic Grunt',
            'commander': 'Galactic Commander',
            'boss': 'Galactic Boss'
        }
        return trainer_tier_tag_map.get(stats.encounter_tier)


def get_tags(stats, is_evolution=False):
    return [
        tag for tag in
        [
            "Pokemon Card",
            stats.biome,
            stats.climate,
            get_encounter_tier_tag(stats, is_evolution)
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
        'health': stats.health,
        'initiative': stats.initiative,
        'types': get_lua_table_from_fields((stats.type_1, stats.type_2)),
        'moves': get_lua_table_from_fields((stats.move_1, stats.move_2, stats.move_3, stats.move_4)),
        'evolve_into': get_lua_table_from_field(stats.evolve_into),
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
    card_json['CustomDeck']['1']['FaceURL'] = CARD_FRONTS_DECK_CLOUD_URLS[j]
    card_json['CustomDeck']['1']['BackURL'] = CARD_BACKS_DECK_CLOUD_URLS[j]

    return card_json


def add_card_to_deck(deck_json, i, j, stats, is_evolution=False):
    card_json = get_card_json(i, j, stats, is_evolution)
    deck_json['ObjectStates'][0]['DeckIDs'].append(100 + i)
    deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)


def run():
    print('Generating deck objects:')
    DECKS_OBJECTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    i, j = 0, 0

    df = read_cube()
    deck_json = get_deck_json()
    output_path = DECKS_OBJECTS_OUTPUT_DIR / DECK_OBJECTS.format(j=j)
    for _, stats in df.iterrows():
        if i == 70:
            with open(output_path, 'w') as f:
                json.dump(deck_json, f)
            i = 0
            j += 1
            deck_json = get_deck_json(j)
            output_path = DECKS_OBJECTS_OUTPUT_DIR / DECK_OBJECTS.format(j=j)

        for k in range(stats.number_in_deck):
            add_card_to_deck(deck_json, i, j, stats, is_evolution=(k != 0))

        i += 1
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)


if __name__ == '__main__':
    run()
