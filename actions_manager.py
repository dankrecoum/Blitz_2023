from dataclasses import dataclass
from typing import List, Dict

from actions import BuildAction, SellAction, SendReinforcementsAction
from game_message import Map, Shop, TowerType, Position, EnemyType


def find_best_position():
    return Position(0, 0)


def find_best_enemy_type():
    return EnemyType.LVL1


class ActionManager:
    def __init__(self, _map):
        self._map = _map
        self.path = []
        self.actions_queue = list()

    def add_tour(self):
        position: Position = find_best_position()
        self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))

    def sell_action(self):
        position: Position = find_best_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))

