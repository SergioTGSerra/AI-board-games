from typing import Optional

from games.spangles.action import SpanglesAction
from games.spangles.result import SpanglesResult
from games.state import State


class SpanglesState(State):
    EMPTY_CELL = -1  # É possivel Jogar nesta cell
    BLOCKED_CELL = -2  # Não é possivel Jogar nesta cell

    def __init__(self, num_rows: int = 2, num_cols: int = 3):
        super().__init__()

        if num_rows < 2:
            raise Exception("the number of rows must be 2 or over")
        if num_cols < 3:
            raise Exception("the number of cols must be 3 or over")

        """
        the dimensions of the board (initial)
        """
        self.__num_rows = num_rows
        self.__num_cols = num_cols

        """
        the grid
        """
        self.__grid = [[SpanglesState.BLOCKED_CELL for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        """
        estados das peças da grid 1 - em pe, 0 - ao contrario
        """
        self.__statePiece = [[0 for _i in range(self.__num_cols)] for _j in range(self.__num_rows)]

        """
        counts the number of turns in the current game
        """
        self.__turns_count = 1

        """
        the index of the current acting player (a peça do primeiro jogador é adicionada automaticamente)
        """
        self.__acting_player = 0

        """
        define na matriz celulaa possiveis ao lado da peça inicial
        """
        self.__grid[0][1] = SpanglesState.EMPTY_CELL
        self.__grid[1][1] = SpanglesState.EMPTY_CELL

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

    def __check_winner(self, player):
        # check for 3 down
        for row in range(0, self.__num_rows - 2):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and self.__statePiece[row][col] == 0 and\
                        self.__grid[row][col + 2] == player and self.__statePiece[row][col] == 0 and \
                        self.__grid[row + 1][col + 1] == player and self.__statePiece[row][col] == 0:
                    return True

        # check for 3 up
        for row in range(2, self.__num_rows):
            for col in range(0, self.__num_cols - 2):
                if self.__grid[row][col] == player and self.__statePiece[row][col] == 1 and\
                        self.__grid[row][col + 2] == player and self.__statePiece[row][col] == 1 and\
                        self.__grid[row - 1][col + 1] == player and self.__statePiece[row][col] == 1:
                    return True

        return False

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: SpanglesAction) -> bool:
        if action is None:
            return False
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

        # Encontra a peça mais próxima com o valor 0 ou 1 na grid antes de defenir a nova jogada
        nearest = None
        for i in range(max(0, row - 1), min(self.__num_rows, row + 2)):
            for j in range(max(0, col - 1), min(self.__num_cols, col + 2)):
                if self.__grid[i][j] in [0, 1]:
                    if nearest is None or abs(i - row) + abs(j - col) < abs(nearest[0] - row) + abs(nearest[1] - col):
                        nearest = (i, j)

        # Faz a jogada
        self.__grid[row][col] = self.__acting_player

        if nearest and nearest[0] < row:
            # peça colocada a baixo da mais proxima
            if self.__statePiece[nearest[0]][nearest[1]] == 1:
                self.__statePiece[row][col] = 0
            elif self.__statePiece[nearest[0]][nearest[1]] == 0:
                self.__statePiece[row][col] = 1
        elif nearest and nearest[0] > row:
            # peça colocada a acima da mais proxima
            if self.__statePiece[nearest[0]][nearest[1]] == 1:
                self.__statePiece[row][col] = 0
            elif self.__statePiece[nearest[0]][nearest[1]] == 0:
                self.__statePiece[row][col] = 1
        elif nearest and nearest[1] < col:
            # peça colocada a direita da mais proxima
            if self.__statePiece[nearest[0]][nearest[1]] == 1:
                self.__statePiece[row][col] = 0
            elif self.__statePiece[nearest[0]][nearest[1]] == 0:
                self.__statePiece[row][col] = 1
        elif nearest and nearest[1] > col:
            # peça colocada a direita da mais proxima
            if self.__statePiece[nearest[0]][nearest[1]] == 1:
                self.__statePiece[row][col] = 0
            elif self.__statePiece[nearest[0]][nearest[1]] == 0:
                self.__statePiece[row][col] = 1

        # Verifica se está a jogar na ultima linha da matriz se sim vai adicionar mais uma linha abaixo
        if len(self.__grid) - 1 == row and len(self.__statePiece) - 1 == row:
            self.__grid.append([SpanglesState.BLOCKED_CELL] * self.__num_cols)
            self.__statePiece.append([0] * self.__num_cols)
            self.__num_rows += 1

        # Verifica se está a jogar na primeira linha da matriz se sim vai adicionar mais uma linha acima
        if row == 0:
            self.__grid.insert(0, [SpanglesState.BLOCKED_CELL] * self.__num_cols)
            self.__statePiece.insert(0, [0] * self.__num_cols)
            self.__num_rows += 1

        # Verifica se está a jogar na ultima coluna da matriz se sim vai adicionar mais uma coluna a direira
        if len(self.__grid[0]) - 1 == col and len(self.__statePiece[0]) - 1 == col:
            for i in range(len(self.__grid)):
                self.__grid[i].append(SpanglesState.BLOCKED_CELL)
            for i in range(len(self.__statePiece)):
                self.__statePiece[i].append(0)
            self.__num_cols += 1

        # Verifica se está a jogar na primeira coluna da matriz se sim vai adicionar mais uma coluna a esquerda
        if col == 0:
            for i in range(len(self.__grid)):
                self.__grid[i].insert(0, SpanglesState.BLOCKED_CELL)
            for i in range(len(self.__statePiece)):
                self.__statePiece[i].insert(0, 0)
            self.__num_cols += 1

        # Percorre a grade para definir os valores das casa impossivceis abaixo e acima
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                if self.__grid[row][col] == 0 or self.__grid[row][col] == 1:
                    #Adiciona casas impossiveis para cima e para baixo
                    if self.__statePiece[row][col] == 1 and self.__grid[row + 1][col] == -2:
                        self.__grid[row + 1][col] = -1
                    elif self.__statePiece[row][col] == 0 and self.__grid[row - 1][col] == -2:
                        self.__grid[row - 1][col] = -1
                    # Adiciona casas impossiveis para direita e para esquerda
                    if self.__statePiece[row][col] == 1 and self.__grid[row][col + 1] == -2:
                        self.__grid[row][col + 1] = -1
                    if self.__statePiece[row][col] == 1 and self.__grid[row][col - 1] == -2:
                        self.__grid[row][col - 1] = -1
                    if self.__statePiece[row][col] == 0 and self.__grid[row][col - 1] == -2:
                        self.__grid[row][col - 1] = -1
                    if self.__statePiece[row][col] == 0 and self.__grid[row][col + 1] == -2:
                        self.__grid[row][col + 1] = -1


        # determine if there is a winner
        self.__has_winner = self.__check_winner(self.__acting_player)

        # switch to next player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

        self.__turns_count += 1

    def __display_cell(self, row, col):
        if self.__grid[row][col] == SpanglesState.EMPTY_CELL:
            print(' ', end="")
        elif self.__grid[row][col] == SpanglesState.BLOCKED_CELL:
            print('x', end="")
        else:
            if self.__statePiece[row][col] == 1 and self.__grid[row][col] == 1:
                print('\033[1;34;48m▲\033[1;m', end="")
            elif self.__statePiece[row][col] == 0 and self.__grid[row][col] == 1:
                print('\033[1;34;48m▼\033[1;m', end="")
            elif self.__statePiece[row][col] == 1 and self.__grid[row][col] == 0:
                print('\033[1;33;48m▲\033[1;m', end="")
            elif self.__statePiece[row][col] == 0 and self.__grid[row][col] == 0:
                print('\033[1;33;48m▼\033[1;m', end="")

    def __display_numbers(self):
        print('  ', end="")
        for col in range(0, self.__num_cols):
            if col < 10:
                print(' ', end="")
            print(col, end="")
        print("")

    def display(self):
        self.__display_numbers()
        for row in range(0, self.__num_rows):
            print(row, '|', end="")
            for col in range(0, self.__num_cols):
                self.__display_cell(row, col)
                print('|', end="")
            print("")
        print("")

    def __is_full(self):
        return self.__turns_count >= 50

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
                cloned_state.__statePiece[row][col] = self.__statePiece[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[SpanglesResult]:
        if self.__has_winner:
            return SpanglesResult.LOOSE if pos == self.__acting_player else SpanglesResult.WIN
        if self.__turns_count >= 50:
            return SpanglesResult.DRAW
        return None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols

    def before_results(self):
        pass

    def get_possible_actions(self) -> set:
        actions = set()
        num_rows, num_cols = self.get_num_rows(), self.get_num_cols()

        for col in range(num_cols):
            for row in range(num_rows):
                action = SpanglesAction(col, row)
                if self.validate_action(action):
                    actions.add(action)

        return actions

    def sim_play(self, action):
        new_state = self.clone()
        new_state.play(action)
        return new_state
