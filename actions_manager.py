from actions import BuildAction, SellAction, SendReinforcementsAction
from dataclasses import dataclass
from dataclasses import dataclass
from game_message import *
from game_message import Map, Shop, TowerType, Position, EnemyType
from typing import List, Dict
from typing import List, Dict

class ActionManager:
    def __init__(self, game_message: GameMessage):
        self.game_message: GameMessage = game_message
        self.paths = list()
        self.starter_position: Position = game_message.map.paths[0].tiles[0]
        self.actions_queue = list()
        self.id = game_message.teamId
        self.our_play_area = game_message.playAreas[self.id]

    def add_tower(self):
        position: Position = self.find_tower_position()
        tower_type = TowerType.SPIKE_SHOOTER
        self.actions_queue.append(BuildAction(tower_type, position))

    def sell_action(self):
        position: Position = self.find_tower_to_sell_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = self.find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))

    def find_tower_to_sell_position(self):
        return Position(0, 0)

    def find_tower_position(self):
        path_start = self.starter_position
        # add support for multiple paths
        # get surrounding positions according to type
        # assuming that we launch a spike shooter
        landing_area: [Position] = self.get_tower_area(TowerType.SPIKE_SHOOTER, path_start)
        # get first position available in landing area
        available_positions = [position for position in landing_area if self.is_position_available(position)]
        print(available_positions)
        return available_positions[0]

    def find_best_enemy_type(self):
        return EnemyType.LVL1

    def get_tower_area(self, tower_type: TowerType, area_center: Position):
        x = area_center.x
        y = area_center.y
        if tower_type == TowerType.SPIKE_SHOOTER:
            positions = [
                Position(x - 1, y - 1),
                Position(x, y - 1),
                Position(x + 1, y - 1),
                Position(x - 1, y),
                Position(x + 1, y),
                Position(x - 1, y + 1),
                Position(x, y + 1),
                Position(x + 1, y + 1)
            ]
        else:  # add other tower types
            positions = [
                Position(x, y)
            ]

        positions = [position for position in positions if
                     0 <= position.x <= self.game_message.map.width and 0 <= position.y <= self.game_message.map.height]

        return positions

    def is_position_available(self, position: Position):
        return not position.y in self.our_play_area.grid[position.x]