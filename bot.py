from actions_manager import ActionManager
from game_message import *
from actions import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
        actions_manager = ActionManager(game_message.map)
        actions_manager.sell_action()
        actions_manager.add_tour()

        if other_team_ids:
            actions_manager.send_reinforcement(other_team_ids[0])

        return actions_manager.actions_queue
