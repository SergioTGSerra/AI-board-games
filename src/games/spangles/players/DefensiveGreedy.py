from random import choice
from games.spangles.action import SpanglesAction
from games.spangles.player import SpanglesPlayer
from games.spangles.state import SpanglesState

from games.state import State


class DefensiveGreedySpanglesPlayer(SpanglesPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: SpanglesState):
        grid = state.get_grid()
        current_pos = self.get_current_pos()
        num_rows = state.get_num_rows()
        num_cols = state.get_num_cols()

        # Tentar formar grupos de peças para maximizar a captura de peças do adversário.
        selected_col = None
        selected_row = None
        max_count = 0

        for col in range(num_cols):
            for row in range(num_rows):
                if not state.validate_action(SpanglesAction(col, row)):
                    continue

                count = 0
                for r in range(num_rows):
                    if grid[r][col] == current_pos:
                        count += 1

                for c in range(num_cols):
                    if grid[row][c] == current_pos:
                        count += 1

                if row == col:
                    for i in range(num_rows):
                        if grid[i][i] == current_pos:
                            count += 1

                if row + col == num_rows - 1:
                    for i in range(num_rows):
                        if grid[i][num_rows - 1 - i] == current_pos:
                            count += 1

                if count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    selected_row = row
                    max_count = count

        # Tentar ocupar as posições centrais do tabuleiro para ter mais opções de jogadas.
        if selected_col is None or selected_row is None:
            if num_rows % 2 == 0:
                middle_rows = [num_rows // 2 - 1, num_rows // 2]
            else:
                middle_rows = [num_rows // 2]

            if num_cols % 2 == 0:
                middle_cols = [num_cols // 2 - 1, num_cols // 2]
            else:
                middle_cols = [num_cols // 2]

            for row in middle_rows:
                for col in middle_cols:
                    if state.validate_action(SpanglesAction(col, row)):
                        selected_col = col
                        selected_row = row
                        break

                if selected_col is not None and selected_row is not None:
                    break

        # Tentar prever a jogada do adversário e bloqueá-la antes que ele tenha a chance de fazê-la.
        if selected_col is None or selected_row is None:
            for col in range(num_cols):
                for row in range(num_rows):
                    if not state.validate_action(SpanglesAction(col, row)):
                        continue

                    new_grid = [row.copy() for row in grid]
                    new_grid[row][col] = current_pos
                    new_state = SpanglesState(new_grid, state.get_acting_player() + 1)
                    if new_state.get_result() == current_pos:
                        selected_col = col
                        selected_row = row
                        break

                if selected_col is not None and selected_row is not None:
                    break

        # Escolher aleatoriamente entre as posições possíveis.
        if selected_col is None or selected_row is None:
            valid_actions = state.get_possible_actions()
            return choice(valid_actions)

        return SpanglesAction(selected_col, selected_row)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass