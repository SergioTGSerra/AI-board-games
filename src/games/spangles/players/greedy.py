from random import choice
from games.spangles.action import SpanglesAction
from games.spangles.player import SpanglesPlayer
from games.spangles.state import SpanglesState

from games.state import State


class GreedySpanglesPlayer(SpanglesPlayer):
    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: SpanglesState):
        grid = state.get_grid()

        # Inicializa variáveis para armazenar a posição selecionada e a contagem máxima
        selected_col = None
        selected_row = None
        max_count = 0

        # Percorre todas as posições possíveis no tabuleiro
        for col in range(0, state.get_num_cols()):
            for row in range(0, state.get_num_rows()):
                # Verifica se a posição é válida
                if not state.validate_action(SpanglesAction(col, row)):
                    continue

                # Inicializa contagem para a posição atual
                count = 0

                # Verifica quantas peças adjacentes na horizontal
                for i in range(-1, 2):
                    if col + i < 0 or col + i >= state.get_num_cols() or i == 0:
                        continue
                    if grid[row][col + i] == state.get_acting_player():
                        count += 1

                # Verifica quantas peças adjacentes na vertical
                for j in range(-1, 2):
                    if row + j < 0 or row + j >= state.get_num_rows() or j == 0:
                        continue
                    if grid[row + j][col] == state.get_acting_player():
                        count += 1

                # Verifica se a posição atual tem uma contagem maior do que a máxima encontrada até agora
                # Se sim, atualiza a posição selecionada e a contagem máxima
                if selected_col is None or count > max_count or (count == max_count and choice([False, True])):
                    selected_col = col
                    selected_row = row
                    max_count = count

        # Se não houver nenhuma posição válida no tabuleiro, gera uma exceção
        if selected_col is None or selected_row is None:
            raise Exception("There is no valid action")

        # Retorna a ação selecionada
        return SpanglesAction(selected_col, selected_row)


    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass