from games.game_simulator import GameSimulator
from games.spangles.players.greedy import GreedySpanglesPlayer
from games.spangles.players.human import HumanSpanglesPlayer
from games.spangles.players.minimax import MinimaxSpanglesPlayer
from games.spangles.players.random import RandomSpanglesPlayer
from games.spangles.simulator import SpanglesSimulator


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("ESTG IA Games Simulator")

    num_iterations = 1000

    # c4_simulations = [
    #     uncomment to play as human
    #     {
    #             "name": "Connect4 - Human VS Random",
    #             "player1": HumanConnect4Player("Human"),
    #             "player2": RandomConnect4Player("Random")
    #     }
    #     {
    #         "name": "Connect4 - Random VS Random",
    #         "player1": RandomConnect4Player("Random 1"),
    #         "player2": RandomConnect4Player("Random 2")
    #     },
    #     {
    #         "name": "Connect4 - Greedy VS Random",
    #         "player1": GreedyConnect4Player("Greedy"),
    #         "player2": RandomConnect4Player("Random")
    #     },
    #     {
    #         "name": "Connect4 - Minimax VS Random",
    #         "player1": MinimaxConnect4Player("Minimax"),
    #         "player2": RandomConnect4Player("Random")
    #     },
    #     {
    #         "name": "Connect4 - Minimax VS Greedy",
    #         "player1": MinimaxConnect4Player("Minimax"),
    #         "player2": GreedyConnect4Player("Greedy")
    #     }
    # ]

    # poker_simulations = [
    #     # uncomment to play as human
    #     #{
    #     #    "name": "Connect4 - Human VS Random",
    #     #    "player1": HumanKuhnPokerPlayer("Human"),
    #     #    "player2": RandomKuhnPokerPlayer("Random")
    #     #},
    #     {
    #         "name": "Kuhn Poker - Random VS Random",
    #         "player1": RandomKuhnPokerPlayer("Random 1"),
    #         "player2": RandomKuhnPokerPlayer("Random 2")
    #     },
    #     {
    #         "name": "Kuhn Poker - AlwaysBet VS Random",
    #         "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
    #         "player2": RandomKuhnPokerPlayer("Random")
    #     },
    #     {
    #         "name": "Kuhn Poker - AlwaysPass VS Random",
    #         "player1": AlwaysPassKuhnPokerPlayer("AlwaysPass"),
    #         "player2": RandomKuhnPokerPlayer("Random")
    #     },
    #     {
    #         "name": "Kuhn Poker - AlwaysBet VS AlwaysPass",
    #         "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
    #         "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
    #     },
    #     {
    #         "name": "Kuhn Poker - AlwaysBet VS AlwaysBetKing",
    #         "player1": AlwaysBetKuhnPokerPlayer("AlwaysBet"),
    #         "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
    #     },
    #     {
    #         "name": "Kuhn Poker - CFR VS Random",
    #         "player1": CFRKuhnPokerPlayer("CFR"),
    #         "player2": RandomKuhnPokerPlayer("Random")
    #     },
    #     {
    #         "name": "Kuhn Poker - CFR VS AlwaysPass",
    #         "player1": CFRKuhnPokerPlayer("CFR"),
    #         "player2": AlwaysPassKuhnPokerPlayer("AlwaysPass")
    #     },
    #     {
    #         "name": "Kuhn Poker - CFR VS AlwaysBet",
    #         "player1": CFRKuhnPokerPlayer("CFR"),
    #         "player2": AlwaysBetKuhnPokerPlayer("AlwaysBet")
    #     },
    #     {
    #         "name": "Kuhn Poker - CFR VS AlwaysBetKing",
    #         "player1": CFRKuhnPokerPlayer("CFR"),
    #         "player2": AlwaysBetKingKuhnPokerPlayer("AlwaysBetKing")
    #     }
    #  ]

    # tictactoe_simulations = [
    #     uncomment to play as human
    #     {
    #        "name": "TicTacToe - Human VS Random",
    #        "player1": HumanTicTacToePlayer("Human"),
    #        "player2": RandomTicTacToePlayer("Random2")
    #     },
    #     {
    #         "name": "TicTacToe - Random VS Random",
    #         "player1": RandomTicTacToePlayer("Random 1"),
    #         "player2": RandomTicTacToePlayer("Random 2")
    #     },
    #     {
    #         "name": "TicTacToe - Greedy VS Random",
    #         "player1": GreedyTicTacToePlayer("Greedy"),
    #         "player2": RandomTicTacToePlayer("Random")
    #     },
    #      {
    #          "name": "TicTacToe - Minimax VS Random",
    #          "player1": MinimaxTicTacToePlayer("Minimax"),
    #          "player2": RandomTicTacToePlayer("Random")
    #      },
    #     {
    #         "name": "TicTacToe - Minimax VS Greedy",
    #         "player1": MinimaxTicTacToePlayer("Minimax"),
    #         "player2": GreedyTicTacToePlayer("Greedy")
    #     }
    # ]

    spangles_simulations = [
        # uncomment to play as human
        # {
        #    "name": "Spangles - Human VS Human",
        #    "player1": HumanSpanglesPlayer("Human 2"),
        #    "player2": HumanSpanglesPlayer("Human 1")
        # },
        {
           "name": "Spangles - Random VS Random",
           "player1": RandomSpanglesPlayer("Random 2"),
           "player2": RandomSpanglesPlayer("Random 1")
        },
        {
           "name": "Spangles - Greedy VS Greedy",
           "player1": GreedySpanglesPlayer("Greedy 2"),
           "player2": GreedySpanglesPlayer("Greedy 1")
        },
        # {
        #    "name": "Spangles - Minimax VS Minimax",
        #    "player1": MinimaxSpanglesPlayer("Minimax 2"),
        #    "player2": MinimaxSpanglesPlayer("Minimax 1")
        # },
        {
            "name": "Spangles - Greedy VS Random",
            "player1": RandomSpanglesPlayer("Random"),
            "player2": GreedySpanglesPlayer("Greedy")
        },
        {
           "name": "Spangles - Greedy VS Greedy",
           "player1": GreedySpanglesPlayer("Greedy 2"),
           "player2": GreedySpanglesPlayer("Greedy 1")
        },
        {
            "name": "Spangles - Greedy VS Minimax",
            "player1": GreedySpanglesPlayer("Greedy"),
            "player2": MinimaxSpanglesPlayer("Minimax")
        },
        {
            "name": "Spangles - Minimax VS Random",
            "player1": RandomSpanglesPlayer("Random"),
            "player2": MinimaxSpanglesPlayer("Minimax")
        }
    ]

    # for sim in c4_simulations:
    #     run_simulation(sim["name"], Connect4Simulator(sim["player1"], sim["player2"]), num_iterations)
    #
    # for sim in poker_simulations:
    #    run_simulation(sim["name"], KuhnPokerSimulator(sim["player1"], sim["player2"]), num_iterations)

    # for sim in tictactoe_simulations:
    #     run_simulation(sim["name"], TicTacToeSimulator(sim["player1"], sim["player2"]), num_iterations)

    for sim in spangles_simulations:
        run_simulation(sim["name"], SpanglesSimulator(sim["player1"], sim["player2"]), num_iterations)


if __name__ == "__main__":
    main()
