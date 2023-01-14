from actions_manager import ActionManager
from game_message import *
from actions import *


class Bot:
    def __init__(self):
        print("Initializing your super mega duper bot")
        self.actions_manager = ActionManager()

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """

        other_team_ids = [team for team in game_message.teams if team != game_message.teamId]
        self.actions_manager.set_game_message(game_message)

        self.actions_manager.add_tour()

        # if other_team_ids:
        #     actions_manager.send_reinforcement(other_team_ids[0])

        return self.actions_manager.actions_queue
