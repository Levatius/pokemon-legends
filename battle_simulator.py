from itertools import combinations, permutations
from pathlib import Path

import pandas as pd

from type_chart import TYPE_CHART

ROOT_DIR = Path(__file__).parent


class Pokemon:
    def __init__(self, name, types, power, bulk):
        self.name = name
        self.types = types
        self.power = power
        self.bulk = bulk
        self._base_power = power
        self._base_bulk = bulk
        self.wins = 0
        self.lost_to = []

    def attacked_modifier(self, attack_type):
        modifier = 1.0
        for type_ in self.types:
            modifier *= TYPE_CHART[attack_type].get(type_, 1.0)
        return modifier

    def get_best_attack_type(self, enemy_pokemon):
        attack_scores = {}
        # Assume our Pokemon only knows attacks of its own type
        for type_ in self.types:
            attack_scores[type_] = enemy_pokemon.attacked_modifier(type_)
        return max(attack_scores, key=attack_scores.get)

    def attack(self, enemy_pokemon):
        best_attack_type = self.get_best_attack_type(enemy_pokemon)
        attack_modifier = enemy_pokemon.attacked_modifier(best_attack_type)
        enemy_pokemon.bulk -= attack_modifier * self.power

    def restore_stats(self):
        self.power = self._base_power
        self.bulk = self._base_bulk

    def battle_with(self, enemy_pokemon):
        # The battle can at most take 10 turns
        for i in range(10):
            turn_order = sorted([self, enemy_pokemon], key=lambda k: k.power, reverse=True)
            for pokemon_1, pokemon_2 in permutations(turn_order, 2):
                pokemon_1.attack(pokemon_2)
                if pokemon_2.bulk <= 0:
                    pokemon_1.wins += 1
                    pokemon_2.lost_to.append(pokemon_1.name)
                    break

            if self.bulk <= 0 or enemy_pokemon.bulk <= 0:
                break

        self.restore_stats()
        enemy_pokemon.restore_stats()


if __name__ == '__main__':
    sinnoh_cube = pd.read_excel(ROOT_DIR / 'sinnoh_cube.xlsx', sheet_name='sinnoh', nrows=160)
    pokemons = []
    for _, row in sinnoh_cube.iterrows():
        pokemon = Pokemon(
            name=row.pokedex_name,
            types=[type_ for type_ in [row.type_1, row.type_2] if not pd.isnull(type_)],
            power=row.power,
            bulk=row.bulk
        )
        pokemons.append(pokemon)

    for pokemon_1, pokemon_2 in combinations(pokemons, 2):
        print(f'{pokemon_1.name} is battling {pokemon_2.name}!')
        pokemon_1.battle_with(pokemon_2)

    results = sorted(pokemons, key=lambda k: k.wins, reverse=True)
    for pokemon in results[:20]:
        print(f'{pokemon.name}: {pokemon.wins} wins, lost to {pokemon.lost_to}')
