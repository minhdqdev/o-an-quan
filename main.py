from game import Game

if __name__ == "__main__":
    print("+----- O AN QUAN -----+\n\n")

    game = Game(algo_0=None, algo_1="expectimax")
    # game = Game(algo_0="expectimax",algo_1="alpha_beta")
    # game = Game(algo_0="random", algo_1="expectimax")
    # game = Game(algo_0="random",algo_1="alpha_beta")
    # game = Game(algo_0="random",algo_1="random")
    
    game.run()

