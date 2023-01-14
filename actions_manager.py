from dataclasses import dataclass
from typing import List, Dict

from actions import BuildAction, SellAction, SendReinforcementsAction
from game_message import *


def find_best_position():
    return Position(0, 0)


def find_best_enemy_type():
    return EnemyType.LVL1


class ActionManager:
    def __init__(self):
        self.void_paths = None
        self.rights_angles_paths = None
        self.parallels_paths = None
        self.actions_queue = None
        self.path = None
        self.our_play_area = None
        self._map = None
        self.id = None
        self.game_message = None

    def set_game_message(self, gameMessage):
        self.game_message = gameMessage
        self.id = gameMessage.teamId
        self._map = gameMessage.map
        self.our_play_area = gameMessage.playAreas[self.id]
        self.path = []
        self.actions_queue = list()
        self.parallels_paths = self.is_there_are_parallels_paths()
        self.rights_angles_paths = self.is_there_right_angles_paths()
        self.void_paths = self.fill_the_void()
    def add_tour(self):
        position: Position = find_best_position()


        [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.rights_angles_paths]
        [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.parallels_paths]
        [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.void_paths]

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
            if tile.y + 2 < self._map.height:
                if Position(tile.x, tile.y + 2) in tiles and not tile.y + 1 in self.our_play_area.grid[tile.x]:
                    available_paths.add(Position(tile.x, tile.y + 1))
            if tile.y - 2 >= 0:
                if Position(tile.x, tile.y - 2) in tiles and not tile.y - 1 in self.our_play_area.grid[tile.x]:
                    available_paths.add(Position(tile.x, tile.y - 1))
            if tile.x + 2 < self._map.width:
                if Position(tile.x + 2, tile.y) in tiles and not tile.y in self.our_play_area.grid[tile.x + 1]:
                    available_paths.add(Position(tile.x + 1, tile.y))
            if tile.x - 2 >= 0:
                if Position(tile.x - 2, tile.y) in tiles and not tile.y in self.our_play_area.grid[tile.x - 1]:
                    available_paths.add(Position(tile.x - 1, tile.y))
        return available_paths

    def is_there_right_angles_paths(self):
        available_paths = set()
        tiles = [tiles for path in self._map.paths for tiles in path.tiles]
        for tile in tiles:
            if tile.y + 1 < self._map.height and tile.x + 1 < self._map.width:
                if Position(tile.x, tile.y + 1) in tiles and Position(tile.x + 1, tile.y) in tiles and not tile.y + 1 in self.our_play_area.grid[tile.x + 1]:
                    available_paths.add(Position(tile.x + 1, tile.y + 1))
            if tile.x - 1 >= 0 and tile.y + 1 < self._map.height:
                if Position(tile.x, tile.y + 1) in tiles and Position(tile.x - 1, tile.y) in tiles and not tile.y + 1 in self.our_play_area.grid[tile.x - 1]:
                    available_paths.add(Position(tile.x - 1, tile.y + 1))
            if tile.x - 1 >= 0 and tile.y - 1 >= 0:
                if Position(tile.x - 1, tile.y) in tiles and Position(tile.x, tile.y - 1) in tiles and not tile.y - 1 in self.our_play_area.grid[tile.x - 1]:
                    available_paths.add(Position(tile.x - 1, tile.y - 1))
            if tile.x + 1 < self._map.width and tile.y - 1 >= 0:
                if Position(tile.x + 1, tile.y) in tiles and Position(tile.x, tile.y - 1) in tiles and not tile.y - 1 in self.our_play_area.grid[tile.x + 1]:
                    available_paths.add(Position(tile.x + 1, tile.y - 1))
        return available_paths

    def fill_the_void(self):
        available_paths = set()
        tiles = [tiles for path in self._map.paths for tiles in path.tiles]
        for tile in tiles:
            if tile.y + 1 < self._map.height:

                if not Position(tile.x, tile.y + 1) in tiles and (not tile.x in self.our_play_area.grid or not tile.y + 1 in self.our_play_area.grid[tile.x]):
                    available_paths.add(Position(tile.x, tile.y + 1))
            if tile.x + 1 < self._map.width:
                if not Position(tile.x + 1, tile.y) in tiles and (not tile.x + 1 in self.our_play_area.grid or not tile.y in self.our_play_area.grid[tile.x + 1]):
                    available_paths.add(Position(tile.x + 1, tile.y))
            if tile.x - 1 >= 0:
                if not Position(tile.x - 1, tile.y) in tiles and (not tile.x - 1 in self.our_play_area.grid or not tile.y in self.our_play_area.grid[tile.x - 1]):
                    available_paths.add(Position(tile.x - 1, tile.y))
            if tile.y - 1 >= 0:
                if not Position(tile.x, tile.y - 1) in tiles and (not tile.x in self.our_play_area.grid or not tile.y - 1 in self.our_play_area.grid[tile.x]):
                    available_paths.add(Position(tile.x, tile.y - 1))
            if tile.y + 1 < self._map.height and tile.x + 1 < self._map.width:
                if not Position(tile.x + 1, tile.y + 1) in tiles and (not tile.x + 1 in self.our_play_area.grid or not tile.y + 1 in self.our_play_area.grid[tile.x + 1]):
                    available_paths.add(Position(tile.x + 1, tile.y + 1))
            if tile.x + 1 < self._map.width and tile.y - 1 >= 0:
                if not Position(tile.x + 1, tile.y - 1) in tiles and (not tile.x + 1 in self.our_play_area.grid or not tile.y - 1 in self.our_play_area.grid[tile.x + 1]):
                    available_paths.add(Position(tile.x + 1, tile.y - 1))
            if tile.x - 1 >= 0 and tile.y + 1 < self._map.height:
                if not Position(tile.x - 1, tile.y + 1) in tiles and (not tile.x - 1 in self.our_play_area.grid or not tile.y + 1 in self.our_play_area.grid[tile.x - 1]):
                    available_paths.add(Position(tile.x - 1, tile.y + 1))
            if tile.x - 1 >= 0 and tile.y - 1 >= 0:
                if not Position(tile.x - 1, tile.y - 1) in tiles and (not tile.x in self.our_play_area.grid or not tile.y - 1 in self.our_play_area.grid[tile.x]):
                    available_paths.add(Position(tile.x - 1, tile.y - 1))
        return available_paths


