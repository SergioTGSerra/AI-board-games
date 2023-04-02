from games.spangles.player import SpanglesPlayer
from games.spangles.state import SpanglesState
from games.game_simulator import GameSimulator


class SpanglesSimulator(GameSimulator):

    def __init__(self, player1: SpanglesPlayer, player2: SpanglesPlayer, num_rows: int = 3, num_cols: int = 5):
        super(SpanglesSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the Spangles grid
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

    def init_game(self):
        return SpanglesState(self.__num_rows, self.__num_cols)

    def before_end_game(self, state: SpanglesState):
        # ignored for this simulator
        pass

    def end_game(self, state: SpanglesState):
        # ignored for this simulator
        pass
