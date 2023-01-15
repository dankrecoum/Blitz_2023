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
        self.void_paths:list = None
        self.rights_angles_paths:list = None
        self.parallels_paths:list = None
        self.actions_queue = None
        self.path = None
        self.our_play_area = None
        self._map = None
        self.id = None
        self.game_message = None

    def set_game_message(self, gameMessage: GameMessage):
        self.game_message: GameMessage = gameMessage
        self.id = gameMessage.teamId
        self._map = gameMessage.map
        self.our_play_area = gameMessage.playAreas[self.id]
        self.path = []
        self.actions_queue = list()

    def set_paths_tower(self):
        self.path = [tiles for path in self._map.paths for tiles in path.tiles]
        self.parallels_paths = list(self.is_there_are_parallels_paths())
        self.rights_angles_paths = list(self.is_there_right_angles_paths())
        self.void_paths = list(self.fill_the_void())
        self.parallels_paths_set = list(self.is_there_are_parallels_paths())
        self.rights_angles_paths_set = list(self.is_there_right_angles_paths())
        self.void_paths_set = list(self.fill_the_void())
    def add_tour(self):
        # a = self.game_message.

        # merge_set = self.rights_angles_paths.union(self.parallels_paths).union(self.void_paths)

        for position in self.rights_angles_paths.copy()[:1]:
            if self.game_message.teamInfos[self.id].money  >= self.game_message.shop.towers[TowerType.SPEAR_SHOOTER].price:
                self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))
                del self.rights_angles_paths[0]
        for position in self.parallels_paths.copy()[:1]:
            if self.game_message.teamInfos[self.id].money  >= self.game_message.shop.towers[TowerType.SPEAR_SHOOTER].price:

                self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))
                del self.parallels_paths[0]
        for position in self.void_paths.copy()[:1]:
            if self.game_message.teamInfos[self.id].money >= self.game_message.shop.towers[TowerType.SPEAR_SHOOTER].price:

                self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position))
                del self.void_paths[0]
        if len(self.rights_angles_paths) == 0 and len(self.parallels_paths) == 0 and len(self.void_paths) == 0:
            for position in self.rights_angles_paths_set.copy()[:1]:
                if self.game_message.teamInfos[self.id].money >= self.game_message.shop.towers[
                    TowerType.SPEAR_SHOOTER].price:
                    self.actions_queue.append(SellAction(position))
                    self.actions_queue.append(BuildAction(TowerType.BOMB_SHOOTER, position))
                    del self.rights_angles_paths_set[0]
            for position in self.parallels_paths_set.copy()[:1]:
                if self.game_message.teamInfos[self.id].money >= self.game_message.shop.towers[
                    TowerType.SPEAR_SHOOTER].price:
                    self.actions_queue.append(SellAction(position))
                    self.actions_queue.append(BuildAction(TowerType.BOMB_SHOOTER, position))
                    del self.parallels_paths_set[0]
            for position in self.void_paths_set.copy()[:1]:
                if self.game_message.teamInfos[self.id].money >= self.game_message.shop.towers[
                    TowerType.SPEAR_SHOOTER].price:
                    self.actions_queue.append(SellAction(position))
                    self.actions_queue.append(BuildAction(TowerType.BOMB_SHOOTER, position))
                    del self.void_paths_set[0]

        # [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in merge_set]
        # [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.parallels_paths]
        # [self.actions_queue.append(BuildAction(TowerType.SPEAR_SHOOTER, position)) for position in self.void_paths]

    def sell_action(self):
        position: Position = find_best_position()
        self.actions_queue.append(SellAction(position))

    def send_reinforcement(self, other_teams_id):
        reinforcement_enemy_type: EnemyType = find_best_enemy_type()
        self.actions_queue.append(SendReinforcementsAction(reinforcement_enemy_type, other_teams_id))

    def is_there_are_parallels_paths(self):
        available_paths = set()
        tiles = self.path
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

    def is_there_right_angles_paths(self) -> set:
        available_paths = set()
        tiles = self.path
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
        tiles = self.path
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


