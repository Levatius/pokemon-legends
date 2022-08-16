import json

import pandas as pd

from config import *
from utils import read_cube


def get_description(stats):
    if pd.isnull(stats.trainer):
        return f'The {stats.classification}'
    else:
        return stats.description


def get_encounter_tier_tag(stats, is_evolution):
    if is_evolution:
        return 'Evolution Card'

    if pd.isnull(stats.trainer):
        encounter_tier_tag_map = {
            'starter': 'Starter Card',
            'weak': 'Weak Encounter Card',
            'moderate': 'Moderate Encounter Card',
            'strong': 'Strong Encounter Card',
            'legendary': 'Legendary Encounter Card',
            'ultra_beast': 'Ultra Beast Encounter Card',
            'ultra_burst': 'Ultra Burst Encounter Card',
            'noble': 'Noble Encounter Card'
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
        'evolve_cost': int(stats.evolve_cost) if not pd.isnull(stats.evolve_into) else 'nil',
        'encounter_tier': f'"{stats.encounter_tier.capitalize()}"',
        'move_name': f'"{stats.move_name}"',
        'move_type': f'"{stats.move_type.capitalize()}"',
        'move_attack_strength': f'"{stats.move_attack_strength}"',
        'move_effect': f'"{stats.move_effect}"'
    }
    lua_script_lines = [f'{variable} = {value}' for variable, value in local_variables.items()]
    return '\n'.join(lua_script_lines)


def get_card_json(deck_json, i, j, stats, is_evolution=False):
    with open(CARD_OBJECT_TEMPLATE) as f:
        card_json = json.load(f)

    card_json['CardID'] = j * 100 + i
    card_json['Nickname'] = stats.pokedex_name + (f' ({stats.description})' if not pd.isnull(stats.description) else '')
    card_json['Description'] = get_description(stats)
    card_json['Tags'] = get_tags(stats, is_evolution)
    card_json['LuaScript'] = get_lua_script(stats)
    card_json['CustomDeck'][str(j)] = {
        'FaceURL': deck_json['ObjectStates'][0]['CustomDeck'][str(j)]['FaceURL'],
        'BackURL': deck_json['ObjectStates'][0]['CustomDeck'][str(j)]['BackURL'],
        'NumWidth': 10,
        'NumHeight': 7,
        'BackIsHidden': True,
        'UniqueBack': True,
        'Type': 0
    }
    return card_json


def add_card_to_deck(deck_json, i, j, k, stats):
    card_json = get_card_json(deck_json, i, j, stats, is_evolution=(k != 0))
    if stats.state == 0:
        deck_json['ObjectStates'][0]['DeckIDs'].append(j * 100 + i)
        deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)
    elif stats.state == 1:
        deck_json['ObjectStates'][0]['DeckIDs'].append(j * 100 + i)
        deck_json['ObjectStates'][0]['ContainedObjects'].append(card_json)
        deck_json['ObjectStates'][0]['ContainedObjects'][-1]['States'] = {}
    elif stats.state > 1:
        deck_json['ObjectStates'][0]['ContainedObjects'][-(k + 1)]['States'][str(stats.state)] = card_json


def run():
    print('Generating deck object:')
    DECK_OBJECT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(DECK_OBJECT_TEMPLATE) as f:
        deck_json = json.load(f)
    output_path = DECK_OBJECT_OUTPUT_DIR / 'deck.json'

    i, j = 0, 0
    for _, stats in read_cube().iterrows():
        if (i == 0 and j == 0) or i == 70:
            deck_json['ObjectStates'][0]['CustomDeck'][str(j + 1)] = {
                'NumWidth': 10,
                'NumHeight': 7,
                'BackIsHidden': True,
                'UniqueBack': True,
                'Type': 0
            }
            face_url = input(f'Enter the Cloud URL for {CARD_FRONTS_DECK_IMG.format(j=j)}:\n')
            deck_json['ObjectStates'][0]['CustomDeck'][str(j + 1)]['FaceURL'] = face_url
            back_url = input(f'Enter the Cloud URL for {CARD_BACKS_DECK_IMG.format(j=j)}:\n')
            deck_json['ObjectStates'][0]['CustomDeck'][str(j + 1)]['BackURL'] = back_url
            i = 0
            j += 1

        for k in range(stats.number_in_deck):
            add_card_to_deck(deck_json, i, j, k, stats)

        i += 1
    else:
        with open(output_path, 'w') as f:
            json.dump(deck_json, f)
    print(
        'Now place the deck.json file found in output/deck_object into your local Documents/My Games/Tabletop Simulator/Saves/Saved Objects folder, you can now import them in Tabletop Simulator by going to Objects -> Saved Objects.')


if __name__ == '__main__':
    run()
