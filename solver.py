import random
from copy import deepcopy
from game import DigitsError


def find_all_solutions(game, steps=5):
    """
    Find all possible solutions to a game, in the form of sequences of games.
     (This isn't a tree, and so contains redundancies when independent steps are played in different orders.)
    :param steps: the number of steps to take. Default 5, which is all possible steps
    :param game: a Game
    :return: list of winning games, all attempts (as a list of lists of games)
    """
    # initialise the games to continue
    games = [[game]]

    # maximum 5 steps total since there are 6 digits
    for m in range(steps):
        # print("steps", m)
        # store the games from this step in here
        all_new_games = []
        # loop through the most recently added games
        for n in range(len(games[-1])):
            # print("\ngame", games[-1][n].field)
            g = games[-1][n]
            # all possible next steps in this game
            new_games = []
            # for one game, try all operations on all pairs of numbers in the field
            for i in range(6-m):  # 6-m since m tracks the step we're on, and at each step we lose a digit
                for j in range(6-m):
                    # + and x are commutative, so just try one. - and / can't work if the second number is biggest.
                    if i != j:
                        for op in g.operations:
                            if g.field[i] > g.field[j] or (g.negatives_allowed and op == '-'):
                                try:
                                    # if the operation works, store a copy
                                    g2 = deepcopy(g)
                                    g2.take_step(g2.field[i], op, g2.field[j])
                                    new_games.append(g2)
                                    # print(i, j, ":", g.field[i], op, g.field[j])
                                    # print(g2.field)
                                except DigitsError:
                                    # if this move is illegal, just skip it
                                    continue
            all_new_games += new_games
        games.append(all_new_games)

    winners = []
    for game_set in games:
        winners += [g for g in game_set if g.won]
    return winners, games


def get_solutions_with_no_remainders(solutions):
    return [g for g in solutions if len(g.field) == 1]


def get_one_step_solutions(g):
    solutions, _ = find_all_solutions(g, 1)
    return solutions




if __name__ == "__main__":

    from game_maker import create_random_game

    # random.seed(10)
    starting_game = create_random_game(maximum_intermediate_result=300)
    print(starting_game)

    print("solving...")
    winners, all_tries = find_all_solutions(starting_game)

    print("total winning games:", len(winners))
    # print(winners[-1])
    winners_no_remainders = [g for g in winners if len(g.field) == 1]
    print("winners with no remainders:", len(winners_no_remainders))
    winners_one_step = [g for g in winners if len(g.field) == 5]
    print("winners in one step:", len(winners_one_step))

    for game in winners_one_step:
        print()
        print(game)
        print(game.history)

