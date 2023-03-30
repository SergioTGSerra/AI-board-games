from random import choice
from games.tictactoe.action import TicTacToeAction
from games.tictactoe.player import TicTacToePlayer
from games.tictactoe.state import TicTacToeState
from games.state import State


class OffensiveGreedyTicTacToePlayer(TicTacToePlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: TicTacToeState):
        grid = state.get_grid()
        dimensions = state.get_dimensions()
        current_pos = self.get_current_pos()

        # Initialize variables for the best move
        best_row = None
        best_col = None
        best_count = -1
        best_positions = []

        # Check each empty position on the board
        for row in range(dimensions):
            for col in range(dimensions):
                if grid[row][col] != "-":
                    continue  # Skip non-empty positions

                count = 0
                positions = []

                # Check row
                for c in range(dimensions):
                    if grid[row][c] == current_pos:
                        count += 1
                    elif grid[row][c] == "-":
                        positions.append((row, c))

                # Check column
                for r in range(dimensions):
                    if grid[r][col] == current_pos:
                        count += 1
                    elif grid[r][col] == "-":
                        positions.append((r, col))

                # Check diagonal (if applicable)
                if row == col:
                    for i in range(dimensions):
                        if grid[i][i] == current_pos:
                            count += 1
                        elif grid[i][i] == "-":
                            positions.append((i, i))

                if row + col == dimensions - 1:
                    for i in range(dimensions):
                        if grid[i][dimensions - 1 - i] == current_pos:
                            count += 1
                        elif grid[i][dimensions - 1 - i] == "-":
                            positions.append((i, dimensions - 1 - i))

                # Update best move
                if count > best_count:
                    best_row = row
                    best_col = col
                    best_count = count
                    best_positions = positions
                elif count == best_count:
                    # If tied, give priority to center positions
                    if (row, col) in [(1, 1), (0, 1), (1, 0), (1, 2), (2, 1)]:
                        best_row = row
                        best_col = col
                        best_positions = positions
                    else:
                        best_positions.extend(positions)

        # Choose random move among the best options
        if len(best_positions) > 0:
            best_pos = choice(best_positions)
            return TicTacToeAction(best_pos[1], best_pos[0])
        else:
            raise Exception("There is no valid action")

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass