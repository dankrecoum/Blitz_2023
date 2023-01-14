from dataclasses import dataclass
from typing import List, Dict

from actions import BuildAction, SellAction, SendReinforcementsAction
from game_message import *


def find_best_position():
    return Position(0, 0)


def find_best_enemy_type():
    return EnemyType.LVL1


class ActionManager:
    def __init__(self, gameMessage: GameMessage):
        self.id = gameMessage.teamId
        self._map = gameMessage.map
        self.our_play_area = gameMessage.playAreas[self.id]
        self.path = []
        self.actions_queue = list()
        self.parallels_paths = self.is_there_are_parallels_paths()

    def add_tour(self):
        position: Position = find_best_position()

        self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))
        # [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.parallels_paths]

    def sell_action(self):
        position: Position = find_best_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))

    def is_there_are_parallels_paths(self):
        available_paths = set()
        tiles = [tiles for path in self._map.paths for tiles in path.tiles]
        for tile in tiles:
            if tile.y + 2 <= self._map.height:
                if Position(tile.x, tile.y + 2) in tiles and not tile.y + 1 in self.our_play_area.grid[tile.x]:
                    available_paths.add(Position(tile.x, tile.y + 1))
            if tile.y - 2 >= 0:
                if Position(tile.x, tile.y - 2) in tiles and not tile.y - 1 in self.our_play_area.grid[tile.x]:
                    available_paths.add(Position(tile.x, tile.y - 1))
            if tile.x + 2 <= self._map.width:
                if Position(tile.x + 2, tile.y) in tiles and not tile.y in self.our_play_area.grid[tile.x + 1]:
                    available_paths.add(Position(tile.x + 1, tile.y))
            if tile.x - 2 >= 0:
                if Position(tile.x - 2, tile.y) in tiles and not tile.y in self.our_play_area.grid[tile.x - 1]:
                    available_paths.add(Position(tile.x - 1, tile.y))
        return available_paths


