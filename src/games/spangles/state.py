from typing import Optional

from games.spangles.action import SpanglesAction
from games.spangles.result import SpanglesResult
from games.state import State


class SpanglesState(State):
    EMPTY_CELL = -1     #É possivel Jogar nesta cell
    BLOCKED_CELL = -2   #Não é possivel Jogar nesta cell

    def __init__(self, num_rows: int = 1, num_cols: int = 1):
        super().__init__()

        if num_rows < 1:
            raise Exception("the number of rows must be 1 or over")
        if num_cols < 1:
            raise Exception("the number of cols must be 1 or over")

        """
        the dimensions of the board (initial)
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols


        """
        the grid
        """
        self.__grid = [[SpanglesState.EMPTY_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player (a peça do primeiro jogador é adicionada automaticamente)
        """
        self.__acting_player = 0

        """
        adiciona a primeira peca para o primeiro jogador ao tabuleiro
        """
        self.__grid[0][1] = self.__acting_player
        self.__acting_player = 1

        """
        define na matriz celulaa bloqueadas longe da peça inicial
        """
        self.__grid[1][2] = SpanglesState.BLOCKED_CELL
        self.__grid[1][0] = SpanglesState.BLOCKED_CELL

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 4 across
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row][col + 1] == player and \
                        self.__grid[row][col + 2] == player and \
                        self.__grid[row][col + 3] == player:
                    return True

        # check for 4 up and down
        for row in range(0, self.__num_rows - 3):
            for col in range(0, self.__num_cols):
                if self.__grid[row][col] == player and \
                        self.__grid[row + 1][col] == player and \
                        self.__grid[row + 2][col] == player and \
                        self.__grid[row + 3][col] == player:
                    return True

        # check upward diagonal
        for row in range(3, self.__num_rows):
            for col in range(0, self.__num_cols - 3):
                if self.__grid[row][col] == player and \
                        self.__grid[row - 1][col + 1] == player and \
                        self.__grid[row - 2][col + 2] == player and \
                        self.__grid[row - 3][col + 3] == player:
                    return True

        # check downward diagonal
        for row in range(0, self.__num_rows - 3):
            for col in range(0, self.__num_cols - 3):
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

    def validate_action(self, action: SpanglesAction) -> bool:
        col = action.get_col()
        row = action.get_row()

        # valid column
        if col < 0 or col >= self.__num_cols:
            return False

        # valid row
        if row < 0 or row >= self.__num_rows:
            return False

        # full column
        if self.__grid[row][col] != SpanglesState.EMPTY_CELL:
            return False

        # valid if cell is possible play
        if self.__grid[row][col] == SpanglesState.BLOCKED_CELL:
            return False

        # apenas pode jogar na celula se o valor for -1
        if self.__grid[row][col] == SpanglesState.EMPTY_CELL:
            return True

        return False

    def update(self, action: SpanglesAction):
        col = action.get_col()
        row = action.get_row()

        self.__grid[row][col] = self.__acting_player

        # Verifica se está a jogar na ultima linha da matriz se sim vai adicionar mais uma linha abaixo
        if len(self.__grid) - 1 == row:
            self.__grid.append([SpanglesState.EMPTY_CELL] * self.__num_cols)
            self.__num_rows += 1

        # Verifica se está a jogar na primeira linha da matriz se sim vai adicionar mais uma linha acima
        if row  == 0:
            self.__grid.insert(0, [SpanglesState.EMPTY_CELL] * self.__num_cols)
            self.__num_rows += 1

        # Verifica se está a jogar na ultima coluna da matriz se sim vai adicionar mais uma coluna a direira
        if len(self.__grid[0]) - 1 == col:
            for i in range(len(self.__grid)):
                self.__grid[i].append(SpanglesState.EMPTY_CELL)
            self.__num_cols += 1

        # Verifica se está a jogar na primeira coluna da matriz se sim vai adicionar mais uma coluna a esuqerda
        if col == 0:
            for i in range(len(self.__grid)):
                self.__grid[i].insert(0, SpanglesState.EMPTY_CELL)
            self.__num_cols += 1

        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        print({
                  0: '0 ',
                  1: '1 ',
                  SpanglesState.EMPTY_CELL: '-1',
                  SpanglesState.BLOCKED_CELL: '-2',
              }[self.__grid[row][col]], end="")

    def display(self):

        for row in range(0, self.__num_rows):
            print('|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
        print("")

    def __is_full(self):
        return self.__turns_count > (self.__num_cols * self.__num_rows)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned_state = SpanglesState(self.__num_rows, self.__num_cols)
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, self.__num_rows):
            for col in range(0, self.__num_cols):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[SpanglesResult]:
        if self.__has_winner:
            return SpanglesResult.LOOSE if pos == self.__acting_player else SpanglesResult.WIN
        if self.__is_full():
            return SpanglesResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self):
        return list(filter(
            lambda action: self.validate_action(action),
            map(
                lambda pos: SpanglesAction(pos, pos),
                range(0, self.get_num_cols()))
        ))

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
