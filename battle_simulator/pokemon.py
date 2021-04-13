from enum import IntEnum

from type_chart import TYPE_CHART


class Pokemon:
    class HealthState(IntEnum):
        FAINTED, INJURED, HEALTHY = range(3)

    def __init__(self, name, types, moves, attack, defence):
        self.name = name
        self.types = types
        self.moves = moves

        self._attack = attack
        self._defence = defence
        self._base_attack = attack
        self._base_defence = defence
        self.health = self.HealthState.HEALTHY

        self.tier = (attack + defence) // 2
        self.points = 0

    @property
    def attack(self):
        return self._attack

    @property
    def defence(self):
        return self._defence

    def has_fainted(self):
        return self.health == self.HealthState.FAINTED

    @staticmethod
    def _get_effectiveness(move, enemy_types):
        effectiveness = 0
        for type_ in enemy_types:
            effectiveness += TYPE_CHART[move].get(type_, 0)
        return effectiveness

    def _get_best_move_against(self, enemy_pokemon):
        move_scores = {}
        for move in self.moves:
            move_scores[move] = self._get_effectiveness(move, enemy_pokemon.types)
        return max(move_scores, key=move_scores.get)

    def _get_attack_damage_with(self, move, enemy_pokemon):
        effectiveness = self._get_effectiveness(move, enemy_pokemon.types)
        stab = 1 if move in self.types else 0
        return self.attack - enemy_pokemon.defence + effectiveness + stab

    def get_attack_damage_to(self, enemy_pokemon):
        best_move = self._get_best_move_against(enemy_pokemon)
        attack_damage = self._get_attack_damage_with(best_move, enemy_pokemon)
        return attack_damage

    def take_damage_effect(self, damage_effect):
        self.health = self.HealthState(self.health - damage_effect if self.health > damage_effect else 0)

    def restore(self):
        self._attack = self._base_attack
        self._defence = self._base_defence
        self.health = self.HealthState.HEALTHY
