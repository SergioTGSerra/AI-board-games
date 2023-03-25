from random import randint

from games.tictactoe.action import TicTacToeAction
from games.tictactoe.player import TicTacToePlayer
from games.tictactoe.state import TicTacToeState
from games.state import State


class RandomTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        return TicTacToeAction(randint(0, state.get_dimensions()), randint(0, state.get_dimensions()))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass


def choice():
    return None