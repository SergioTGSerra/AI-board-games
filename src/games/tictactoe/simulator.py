from games.tictactoe.player import TicTacToePlayer
from games.tictactoe.state import TicTacToeState
from games.game_simulator import GameSimulator


class TicTacToeSimulator(GameSimulator):

    def __init__(self, player1: TicTacToePlayer, player2: TicTacToePlayer, dimension: int = 3):
        super(TicTacToeSimulator, self).__init__([player1, player2])
        """
        the number of rows and cols from the connect4 grid
        """
        self.__dimension = dimension

    def init_game(self):
        return TicTacToeState(self.__dimension)

    def before_end_game(self, state: TicTacToeState):
        # ignored for this simulator
        pass

    def end_game(self, state: TicTacToeState):
        # ignored for this simulator
        pass
