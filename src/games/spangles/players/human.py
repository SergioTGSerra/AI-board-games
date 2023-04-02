from games.spangles.action import SpanglesAction
from games.spangles.player import SpanglesPlayer
from games.spangles.state import SpanglesState


class HumanSpanglesPlayer(SpanglesPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: SpanglesState):
        state.display()
        while True:
            # noinspection PyBroadException
            try:
                return SpanglesAction(int(input(f"Player {state.get_acting_player()}, choose a column: ")))
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: SpanglesState):
        # ignore
        pass

    def event_end_game(self, final_state: SpanglesState):
        # ignore
        pass
