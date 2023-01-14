from actions import BuildAction, SellAction, SendReinforcementsAction
from dataclasses import dataclass
from dataclasses import dataclass
from game_message import *
from game_message import Map, Shop, TowerType, Position, EnemyType
from typing import List, Dict
from typing import List, Dict


def find_best_position():
    return Position(0,0)

def find_starter_position_for_tower(self):
    # # return surrounding position
    # path_start = self.starter_position
    # surround:Position[] = [path_start]
    return self.starter_position.x


def find_best_enemy_type():
    return EnemyType.LVL1

last_position = None
class ActionManager:
    def __init__(self, game_message: GameMessage):
        self.game_message: GameMessage = game_message
        self._map = game_message.map
        self.paths = list()
        self.actions_queue = list()

    def find_best_position_for_spear(self, starter_position):
        accessible_positions = [
            Position(starter_position.x - 2, starter_position.y - 2),
            Position(starter_position.x - 1, starter_position.y - 1),
            Position(starter_position.x, starter_position.y - 2),
            Position(starter_position.x + 1, starter_position.y - 2),
            Position(starter_position.x + 2, starter_position.y - 2),
            Position(starter_position.x + 2, starter_position.y - 1),
            Position(starter_position.x + 2, starter_position.y),
            Position(starter_position.x + 2, starter_position.y + 1),
            Position(starter_position.x + 2, starter_position.y + 2),
            Position(starter_position.x + 1, starter_position.y + 2),
            Position(starter_position.x, starter_position.y + 2),
            Position(starter_position.x - 1, starter_position.y + 2),
            Position(starter_position.x - 2, starter_position.y + 2),
            Position(starter_position.x - 2, starter_position.y + 1),
            Position(starter_position.x - 2, starter_position.y),
            Position(starter_position.x - 2, starter_position.y - 1),
            Position(starter_position.x - 1, starter_position.y - 1),
            Position(starter_position.x, starter_position.y - 1),
            Position(starter_position.x + 1, starter_position.y - 1),
            Position(starter_position.x - 1, starter_position.y),
            Position(starter_position.x + 1, starter_position.y),
            Position(starter_position.x - 1, starter_position.y + 1),
            Position(starter_position.x, starter_position.y + 1),
            Position(starter_position.x + 1, starter_position.y + 1)
        ]

        for possible_position in accessible_positions:
            for path in self.game_message.map.paths:
                if not possible_position in path.tiles:
                    if possible_position.y < self._map.height and possible_position.x < self._map.width and possible_position.x >= 0 and possible_position.y >= 0:
                        return possible_position
        return Position(0, 0)  # default one

    def add_tower(self, position: Position=None):
        if position == None:
            position = self.game_message.map.paths[0].tiles[0]
        position: Position = self.find_best_position_for_spear(position)
        self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))
        return position


    def sell_action(self):
        position: Position = find_best_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))
