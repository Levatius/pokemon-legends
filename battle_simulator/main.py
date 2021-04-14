import random
from collections import Counter
from itertools import combinations
from pathlib import Path

import pandas as pd

from pokemon import Pokemon

ROOT_DIR = Path(__file__).parent.parent
OHKO_THRESHOLD = 7


def initalise_pokemons(tier_lower_bound=1):
    sinnoh_cube = pd.read_excel(ROOT_DIR / 'sinnoh_cube.xlsx', sheet_name='sinnoh')

    pokemons = []
    for _, row in sinnoh_cube.iterrows():
        if row.tier < tier_lower_bound:
            continue

        pokemon = Pokemon(
            name=row.pokedex_name,
            types=[type_ for type_ in [row.type_1, row.type_2] if not pd.isnull(type_)],
            moves=[move for move in [row.move_1, row.move_2, row.move_3] if not pd.isnull(move)],
            attack=row.attack,
            defence=row.defence
        )
        pokemons.append(pokemon)
    return pokemons


class AttackDice:
    @classmethod
    def roll(cls):
        return random.randint(1, 6)


def get_dice_bonus(our_dice_roll, their_dice_roll):
    our_dice_bonus = our_dice_roll - their_dice_roll if our_dice_roll > their_dice_roll else 0
    return our_dice_bonus


def get_damage_effect(total_damage):
    if total_damage >= OHKO_THRESHOLD:
        return 2
    elif total_damage > 0:
        return 1
    return 0


def battle(our_pokemon, their_pokemon):
    our_pokemon.restore()
    their_pokemon.restore()

    # The battle can at most take 10 turns
    for i in range(10):
        our_attack_damage = our_pokemon.get_attack_damage_to(their_pokemon)
        their_attack_damage = their_pokemon.get_attack_damage_to(our_pokemon)

        our_dice_roll = AttackDice.roll()
        their_dice_roll = AttackDice.roll()

        our_dice_bonus = get_dice_bonus(our_dice_roll, their_dice_roll)
        their_dice_bonus = get_dice_bonus(their_dice_roll, our_dice_roll)

        our_damage_effect = get_damage_effect(our_attack_damage + our_dice_bonus)
        their_damage_effect = get_damage_effect(their_attack_damage + their_dice_bonus)

        our_pokemon.take_damage_effect(their_damage_effect)
        their_pokemon.take_damage_effect(our_damage_effect)

        if our_pokemon.has_fainted() or their_pokemon.has_fainted():
            return Counter({
                'pokemon_1_wins': 1 if not our_pokemon.has_fainted() and their_pokemon.has_fainted() else 0,
                'pokemon_2_wins': 1 if our_pokemon.has_fainted() and not their_pokemon.has_fainted() else 0,
                'draws': 1 if our_pokemon.has_fainted() and their_pokemon.has_fainted() else 0,
                'DNE': 0
            })
    return Counter({'pokemon_1_wins': 0, 'pokemon_2_wins': 0, 'draws': 0, 'DNE': 1})


def simulate_all_battle_combinations(pokemons):
    overall_result = Counter({'pokemon_1_wins': 0, 'pokemon_2_wins': 0, 'draws': 0, 'DNE': 0})
    for pokemon_1, pokemon_2 in combinations(pokemons, 2):
        result = Counter({'pokemon_1_wins': 0, 'pokemon_2_wins': 0, 'draws': 0, 'DNE': 0})
        for _ in range(5):
            result += battle(pokemon_1, pokemon_2)
        overall_result += result
        pokemon_1.points += result.get('pokemon_1_wins', 0) + 0.5 * result.get('draws', 0)
        pokemon_2.points += result.get('pokemon_2_wins', 0) + 0.5 * result.get('draws', 0)
        pokemon_1.dne += result.get('DNE', 0)
        pokemon_2.dne += result.get('DNE', 0)
        print(f'{pokemon_1.name} vs {pokemon_2.name}: {result}')
    print(f'Overall: {overall_result}')


def run():
    pokemons = initalise_pokemons(tier_lower_bound=7)
    simulate_all_battle_combinations(pokemons)

    results = sorted(pokemons, key=lambda k: k.points, reverse=True)
    for pokemon in results:
        print(f'{pokemon.name}: {pokemon.points} points, {pokemon.dne} dne')


if __name__ == '__main__':
    run()
