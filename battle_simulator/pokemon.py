import random
from enum import IntEnum

from type_chart import TYPE_CHART


class AttackDice:
    CRITICAL_HIT = ('critical_hit', 6)
    LUCKY_HIT = ('lucky_hit', 4)
    HIT = ('hit', 3)
    STATUS_HIT = ('status_hit', 2)

    @classmethod
    def roll(cls):
        return random.choice([cls.CRITICAL_HIT, cls.LUCKY_HIT, cls.STATUS_HIT, cls.HIT, cls.HIT, cls.HIT])


class Move:
    def __init__(self, name, type_, power=0):
        self.name = name
        self.type_ = type_
        self.power = power

    def get_effectiveness_against(self, enemy_types):
        effectiveness = 0
        for type_ in enemy_types:
            effectiveness += TYPE_CHART[self.type_].get(type_, 0)
        return effectiveness


class HealthState(IntEnum):
    FAINTED, INJURED, HEALTHY = range(3)


class Pokemon:
    INJURED_PENALTY = -2
    OHKO_THRESHOLD = 7

    def __init__(self, name, types, offence, defence):
        self.name = name
        self.types = types

        self._offence = offence
        self._defence = defence
        self._base_offence = offence
        self._base_defence = defence
        self.health = HealthState.HEALTHY

        # Assume our Pokemon only knows attacks of its own type
        self.moves = [Move(f'{type_}_move', type_) for type_ in self.types]

        self.wins = 0
        self.lost_to = []

    @property
    def offence(self):
        return self._offence

    @property
    def defence(self):
        return self._defence + (self.INJURED_PENALTY if self.health == HealthState.INJURED else 0)

    def has_fainted(self):
        return self.health == HealthState.FAINTED

    def _select_best_move_against(self, enemy_pokemon):
        move_scores = {}
        for move in self.moves:
            move_scores[move] = move.get_effectiveness_against(enemy_pokemon.types)
        return max(move_scores, key=move_scores.get)

    def _calculate_attack_damage(self, move, enemy_pokemon):
        effectiveness = move.get_effectiveness_against(enemy_pokemon.types)
        attack_dice_result, attack_dice_bonus = AttackDice.roll()
        return attack_dice_result, self.offence - enemy_pokemon.defence + effectiveness + attack_dice_bonus

    def attack(self, enemy_pokemon):
        best_move = self._select_best_move_against(enemy_pokemon)
        attack_dice_result, attack_damage = self._calculate_attack_damage(best_move, enemy_pokemon)
        if attack_damage >= self.OHKO_THRESHOLD:
            enemy_pokemon.health = HealthState.FAINTED
        elif attack_damage > 0:
            enemy_pokemon.health = HealthState(enemy_pokemon.health - 1)
        print(
            f'{self.name} attacks {enemy_pokemon.name} with {best_move.name} for {attack_damage} damage [{attack_dice_result}]')

    def restore(self):
        self._offence = self._base_offence
        self._defence = self._base_defence
        self.health = HealthState.HEALTHY
