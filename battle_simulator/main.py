from itertools import combinations, permutations
from pathlib import Path

import pandas as pd
# import seaborn as sns

from pokemon import Pokemon

ROOT_DIR = Path(__file__).parent.parent


def initalise_pokemons():
    sinnoh_cube = pd.read_excel(ROOT_DIR / 'sinnoh_cube.xlsx', sheet_name='sinnoh')

    pokemons = []
    for _, row in sinnoh_cube.iterrows():
        pokemon = Pokemon(
            name=row.pokedex_name,
            types=[type_ for type_ in [row.type_1, row.type_2] if not pd.isnull(type_)],
            offence=row.offence,
            defence=row.defence
        )
        pokemons.append(pokemon)
    return pokemons


def battle(pokemon, enemy_pokemon):
    # The battle can at most take 10 turns
    for i in range(10):
        turn_order = sorted([pokemon, enemy_pokemon], key=lambda k: k.offence, reverse=True)
        for pokemon_1, pokemon_2 in permutations(turn_order, 2):
            pokemon_1.attack(pokemon_2)
            if pokemon_2.has_fainted():
                print(f'{pokemon_1.name} has defeated {pokemon_2.name}')
                pokemon_1.wins += 1
                pokemon_2.lost_to.append(pokemon_1.name)
                break

        if pokemon.has_fainted() or enemy_pokemon.has_fainted():
            break

    pokemon.restore()
    enemy_pokemon.restore()


def simulate_all_battle_combinations(pokemons):
    for pokemon_1, pokemon_2 in combinations(pokemons, 2):
        battle(pokemon_1, pokemon_2)


def run():
    pokemons = initalise_pokemons()
    simulate_all_battle_combinations(pokemons)

    results = sorted(pokemons, key=lambda k: k.wins, reverse=True)
    for pokemon in results[:20]:
        print(f'{pokemon.name}: {pokemon.wins} wins, lost to {pokemon.lost_to}')


if __name__ == '__main__':
    run()
