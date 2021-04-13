import random
from itertools import combinations
from pathlib import Path

import pandas as pd

from pokemon import Pokemon

ROOT_DIR = Path(__file__).parent.parent
OHKO_THRESHOLD = 7


def initalise_pokemons():
    sinnoh_cube = pd.read_excel(ROOT_DIR / 'sinnoh_cube.xlsx', sheet_name='sinnoh')

    pokemons = []
    for _, row in sinnoh_cube.iterrows():
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
    if total_damage > OHKO_THRESHOLD:
        return 2
    elif total_damage > 0:
        return 1
    return 0


def battle(our_pokemon, their_pokemon):
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

        if their_pokemon.has_fainted() and not our_pokemon.has_fainted():
            # print(f'{our_pokemon.name} has defeated {their_pokemon.name} in {i} turns')
            our_pokemon.points += 1
            break
        elif our_pokemon.has_fainted() and not their_pokemon.has_fainted():
            # print(f'{their_pokemon.name} has defeated {our_pokemon.name} in {i} turns')
            their_pokemon.points += 1
            break
        elif our_pokemon.has_fainted() or their_pokemon.has_fainted():
            # print(f'{our_pokemon.name} and {their_pokemon.name} have fainted after {i} turns')
            break
    else:
        print(f'{our_pokemon.name} and {their_pokemon.name} ended in a tie')

    our_pokemon.restore()
    their_pokemon.restore()


def simulate_all_battle_combinations(pokemons):
    for pokemon_1, pokemon_2 in combinations(pokemons, 2):
        for _ in range(5):
            battle(pokemon_1, pokemon_2)


def run():
    pokemons = initalise_pokemons()
    simulate_all_battle_combinations(pokemons)

    results = sorted(pokemons, key=lambda k: k.points, reverse=True)
    for pokemon in results[:100]:
        print(f'{pokemon.name}: {pokemon.points} points')


if __name__ == '__main__':
    run()
