from random import choice
from games.tictactoe.action import TicTacToeAction
from games.tictactoe.player import TicTacToePlayer
from games.tictactoe.state import TicTacToeState
from games.state import State


class DefensiveGreedyTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()

        selected_col = None
        selected_row = None
        max_count = 0

        for col in range(0, state.get_dimensions()):
            for row in range(0, state.get_dimensions()):
                if not state.validate_action(TicTacToeAction(col, row)):
                    continue

                count = 0
                for r in range(0, state.get_dimensions()):
                    if grid[r][col] == self.get_current_pos():
                        count += 1

                for c in range(0, state.get_dimensions()):
                    if grid[row][c] == self.get_current_pos():
                        count += 1

                if row == col:
                    for i in range(0, state.get_dimensions()):
                        if grid[i][i] == self.get_current_pos():
                            count += 1

                if row + col == state.get_dimensions() - 1:
                    for i in range(0, state.get_dimensions()):
                        if grid[i][state.get_dimensions() - 1 - i] == self.get_current_pos():
                            count += 1

                if selected_col is None or count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    selected_row = row
                    max_count = count

        if selected_col is None or selected_row is None:
            raise Exception("There is no valid action")

        return TicTacToeAction(selected_col, selected_row)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass