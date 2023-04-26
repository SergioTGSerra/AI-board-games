import math

from games.spangles.player import SpanglesPlayer
from games.spangles.result import SpanglesResult
from games.spangles.state import SpanglesState
from games.state import State


class MinimaxSpanglesPlayer(SpanglesPlayer):

    def __init__(self, name):
        super().__init__(name)

    '''
    This heuristic will simply count the maximum number of consecutive pieces that the player has
    It's not a great heuristic as it doesn't take into consideration a defensive approach
    '''

    def heuristic(state: SpanglesState):
        board = state.get_grid()
        current_player = state.get_acting_player()
        num_cols = state.get_num_cols()
        num_rows = state.get_num_rows()
        score = 0

        # check for 3 in a row
        for row in range(0, num_rows - 2):
            for col in range(0, num_cols - 2):
                if board[row][col] == current_player and state.get_piece_state(row, col) == 0 and \
                        board[row][col + 2] == current_player and state.get_piece_state(row, col + 2) == 0 and \
                        board[row + 1][col + 1] == current_player and state.get_piece_state(row + 1, col + 1) == 0:
                    score += 1

        # check for 3 up
        for row in range(2, num_rows):
            for col in range(0, num_cols - 2):
                if board[row][col] == current_player and state.get_piece_state(row, col) == 1 and \
                        board[row][col + 2] == current_player and state.get_piece_state(row, col + 2) == 1 and \
                        board[row - 1][col + 1] == current_player and state.get_piece_state(row - 1, col + 1) == 1:
                    score += 1

        # check for 4 in a row
        for row in range(0, num_rows):
            count = 0
            for col in range(0, num_cols):
                if board[row][col] == current_player and state.get_piece_state(row, col) == 0:
                    count += 1
                else:
                    if count == 4:
                        score += 1
                    count = 0
            if count == 4:
                score += 1

        # check for 4 in a column
        for col in range(0, num_cols):
            count = 0
            for row in range(0, num_rows):
                if board[row][col] == current_player and state.get_piece_state(row, col) == 0:
                    count += 1
                else:
                    if count == 4:
                        score += 1
                    count = 0
            if count == 4:
                score += 1

        return score

    """Implementation of minimax search (recursive, with alpha/beta pruning) :param state: the state for which the 
    search should be made :param depth: maximum depth of the search :param alpha: to optimize the search :param beta: 
    to optimize the search :param is_initial_node: if true, the function will return the action with max ev, 
    otherwise it return the max ev (ev = expected value) """

    def minimax(self, state: SpanglesState, depth: int, alpha: int = -math.inf, beta: int = math.inf,
                is_initial_node: bool = True):
        # first we check if we are in a terminal node (victory, draw or loose)
        if state.is_finished():
            return {
                SpanglesResult.WIN: 40,
                SpanglesResult.LOOSE: -40,
                SpanglesResult.DRAW: 0
            }[state.get_result(self.get_current_pos())]

        # if we reached the maximum depth, we will return the value of the heuristic
        if depth == 0:
            return self.__heuristic(state)

        # if we are the acting player
        if self.get_current_pos() == state.get_acting_player():
            print(str(self.get_current_pos()) + " | " + str(state.get_acting_player()))
            # very small integer
            value = -math.inf
            selected_action = None

            for action in state.get_possible_actions():
                pre_value = value
                value = max(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value > pre_value:
                    selected_action = action
                if value > beta:
                    break
                alpha = max(alpha, value)

            return selected_action if is_initial_node else value

        # if it is the opponent's turn
        else:
            value = math.inf
            for action in state.get_possible_actions():
                value = min(value, self.minimax(state.sim_play(action), depth - 1, alpha, beta, False))
                if value < alpha:
                    break
                beta = min(beta, value)
            return value

    def get_action(self, state: SpanglesState):
        return self.minimax(state, 5)

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
