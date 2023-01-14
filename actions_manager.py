from actions import BuildAction, SellAction, SendReinforcementsAction
from dataclasses import dataclass
from dataclasses import dataclass
from game_message import *
from game_message import Map, Shop, TowerType, Position, EnemyType
from typing import List, Dict
from typing import List, Dict


def find_best_position():
    return Position(0, 0)


def find_starter_position_for_tower(self):
    # # return surrounding position
    # path_start = self.starter_position
    # surround:Position[] = [path_start]
    return self.starter_position.x


def find_best_enemy_type():
    return EnemyType.LVL1


last_position = None


class ActionManager:
    def __init__(self, game_message: GameMessage, lastPositions):
        self.game_message: GameMessage = game_message
        self.id = game_message.teamId
        self._map = game_message.map
        self.our_play_area = game_message.playAreas[self.id]
        self.paths = list()
        self.lastPositions = lastPositions
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
                if not (possible_position in path.tiles and possible_position in self.lastPositions):
                    if possible_position.y < self._map.height and possible_position.x < self._map.width and possible_position.x >= 0 and possible_position.y >= 0:
                        return possible_position
        return self.is_there_right_angles_paths().pop()  # default one

    def add_tower(self, position: Position = None):
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
