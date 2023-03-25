from typing import Optional

from games.tictactoe.action import TicTacToeAction
from games.tictactoe.result import TicTacToeResult
from games.state import State


class TicTacToeState(State):
    EMPTY_CELL = -1

    def __init__(self, dimension: int = 3):
        super().__init__()

        if dimension < 3:
            raise Exception("the number of dimensions must be 3 or over")

        """
        the dimensions of the board
        """
        self.__dimension = dimension

        """
        the grid
        """
        self.__grid = [[TicTacToeState.EMPTY_CELL for _i in range(self.__dimension)] for _j in range(self.__dimension)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player
        """
        self.__acting_player = 0

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 4 across
        for row in range(0, self.__dimension):
            for col in range(0, self.__dimension - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player and \
                        self.__grid[row][col + 3] == player:
                    return True

        # check for 4 up and down
        for row in range(0, self.__dimension - 3):
            for col in range(0, self.__dimension):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player and \
                        self.__grid[row + 3][col] == player:
                    return True

        # check upward diagonal
        for row in range(3, self.__dimension):
            for col in range(0, self.__dimension - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player and \
                        self.__grid[row - 3][col + 3] == player:
                    return True

        # check downward diagonal
        for row in range(0, self.__dimension - 3):
            for col in range(0, self.__dimension - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col + 1] == player and \
                        self.__grid[row + 2][col + 2] == player and \
                        self.__grid[row + 3][col + 3] == player:
                    return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: TicTacToeAction) -> bool:
        col = action.get_col()

        # valid column
        if col < 0 or col >= self.__dimension:
            return False

        # full column
        if self.__grid[0][col] != TicTacToeState.EMPTY_CELL:
            return False

        return True

    def update(self, action: TicTacToeAction):
        col = action.get_col()
        row = action.get_row()

        self.__grid[row][col] = self.__acting_player

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        print({
                  0: 'R',
                  1: 'B',
                  TicTacToeState.EMPTY_CELL: ' '
              }[self.__grid[row][col]], end="")

    def __display_numbers(self):
        for col in range(0, self.__dimension):
            if col < 10:
                print(' ', end="")
            print(col, end="")
        print("")

    def __display_separator(self):
        for col in range(0, self.__dimension):
            print("--", end="")
        print("-")

    def display(self):
        self.__display_numbers()
        self.__display_separator()

        for row in range(0, self.__dimension):
            print('|', end="")
            for col in range(0, self.__dimension):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
            self.__display_separator()

        self.__display_numbers()
        print("")

    def __is_full(self):
        return self.__turns_count > (self.__dimension * self.__dimension)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = TicTacToeState(self.__dimension)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__dimension):
            for col in range(0, self.__dimension):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[TicTacToeResult]:
        if self.__has_winner:
            return TicTacToeResult.LOOSE if pos == self.__acting_player else TicTacToeResult.WIN
        if self.__is_full():
            return TicTacToeResult.DRAW
        return None

    def get_dimensions(self):
        return self.__dimension

    def before_results(self):
        pass

    def get_possible_actions(self):
        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda pos: TicTacToeAction(pos),
                range(0, self.get_dimensions()))
        ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
