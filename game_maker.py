import random

from game import Game, DigitsError
from solver import find_all_solutions, get_one_step_solutions


def generate_game_without_one_step_solution(maximum_starter=25, maximum_intermediate_result=1000,
                                            maximum_small_starter=10, max_target=500, negatives_allowed=False):
    """
    Generate games until you get one with target below max_target and no single-step solution
    :return: Game
    """
    print("finding a good game...")
    tries = 0
    max_tries = 10  # just to be safe
    game = None
    while tries < max_tries and game is None:
        tries += 1
        g = create_random_game(maximum_starter, maximum_intermediate_result, maximum_small_starter,
                               negatives_allowed=negatives_allowed)
        if g.target > max_target:
            continue
        if len(get_one_step_solutions(g)) == 0:
            game = g

    return game


def create_random_game(maximum_starter=25, maximum_intermediate_result=1000, maximum_small_starter=10,
                       negatives_allowed=False):
    """
    Create a game
    :param maximum_small_starter: half the starting digits are no bigger than this (default 10)
    :param maximum_intermediate_result: the gold solution never has an intermediate result higher than this (default 200)
    :param maximum_starter: starter digits can't be larger than this (default 25)
    :return: Game
    """
    # no 1s allowed
    # half of starters are very small, the other half might be bigger
    starters = random.sample(range(2, maximum_small_starter), k=3)
    starters += random.sample([i for i in range(2, maximum_starter) if i not in starters], k=3)
    game = Game(0, starters, negatives_allowed=negatives_allowed)
    while len(game.field) > 1:
        # print(game)
        op = random.choice(game.operations)
        found = False
        if op == "/":
            tries = 5
        elif op == "-":
            tries = 2
        else:
            tries = 1
        attempt = 0
        while attempt < tries and not found:
            numbers = random.sample(game.field, k=2)
            try:
                result = game.calculate_result(numbers[0], op, numbers[1])
                found = True
                # print("found division!")
            except DigitsError as e:
                # print(e)
                attempt += 1
                continue
            if result > maximum_intermediate_result:
                attempt += 1
                found = False
                continue
        # print(game)
        # print(f"{numbers[0]} {op} {numbers[1]}")
        if found:
            game.take_step(numbers[0], op, numbers[1])
            game.target = result
    return Game(game.target, game.starters, negatives_allowed=negatives_allowed)
