from random import randint

from games.spangles.action import SpanglesAction
from games.spangles.player import SpanglesPlayer
from games.spangles.state import SpanglesState
from games.state import State


class RandomSpanglesPlayer(SpanglesPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: SpanglesState):

        return SpanglesAction(randint(0, state.get_num_cols()), randint(0, state.get_num_rows()))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
