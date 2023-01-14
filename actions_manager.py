from actions import BuildAction, SellAction, SendReinforcementsAction
from dataclasses import dataclass
from dataclasses import dataclass
from game_message import *
from game_message import Map, Shop, TowerType, Position, EnemyType
from typing import List, Dict
from typing import List, Dict


def find_best_position():
    return Position(0,0)

# def find_starter_position_for_tower(self):
#     # # return surrounding position
#     # path_start = self.starter_position
#     # surround:Position[] = [path_start]
#     return self.starter_position.x


def find_best_enemy_type():
    return EnemyType.LVL1


class ActionManager:
    def __init__(self, game_message: GameMessage):
        self.game_message: GameMessage = game_message
        self.paths = list()
        self.starter_position: Position = game_message.map.paths[0].tiles[0]
        self.actions_queue = list()

    def add_tower(self):
        position: Position = find_best_position()
        self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))

    def sell_action(self):
        position: Position = find_best_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))
