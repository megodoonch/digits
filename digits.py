"""
Digits game by Doug and Meaghan

Based on NYTimes Digits game

The player is given 6 natural numbers (n > 0) and a seventh, which is the goal. We have +,-,x,/.
We must stay within N (Natural numbers) at every step.
We need to get the goal with any combinations of the given numbers using the operations.

TODO Possible variants:

    - DONE Must use all digits
    - More operations allowed (square, square root?)
    - Use all of R (Reals: negatives, fractions, square roots...) or Q or at least Z
    - Larger solution space (Z? Q? R?)
    - Different number of starting digits
    - Unique solution
        - solver can't do this now, because it's not a decision tree
    - give countdown from target (Doug will explain)
    - only prime starters

Definitions:
    - target (the number we want to get to)
    - starters (the initial 6 numbers)
    - field (the set of current numbers)

DONE Create a game with a solution (the target and starters)

TODO GUI (ask Soren?)

"""
from game import DigitsError
from game_maker import generate_game_without_one_step_solution, Game


def run_game(my_game: Game, max_steps=None, no_remainders_allowed=False):
    """
    User interface.
    Uses input to interact with player.
    Inputs required to be separated by white space, as in 1 + 2
    :param no_remainders_allowed: if True, win condition requires all digits be used
    :param max_steps: Stop after this many steps. Default 1000000000
    :param my_game: an initialised Game
    """
    if max_steps is None:
        max_steps = 1000000000
    step = 0
    print("Instructions")
    print("\tinput example: 1 + 2")
    if no_remainders_allowed:
        print("\tNo leftover digits allowed!")
    print("\tTo stop the game, type 'exit'")
    print("\tTo undo, type 'undo'")
    print(f"\t{my_game.operations_string()}")
    while step < max_steps:
    # while False:
        step += 1
        print(my_game)

        equation = input("Enter equation: ")

        # rfind returns -1 if the argument isn't found, otherwise the index where it starts, so the player entered
        # exit or quit if it returns 0 or higher
        if equation.lower().rfind("exit") >= 0 or equation.lower().rfind("quit") >= 0:
            print("exiting")
            exit(0)

        if equation.lower() == "undo":
            my_game.undo()
            continue

        try:
            # user input should be int op int
            parts = equation.split()
            first_input_number = int(parts[0])
            input_operation_as_string = parts[1]
            second_input_number = int(parts[2])
            try:
                # try to update the game
                result = my_game.take_step(first_input_number, input_operation_as_string, second_input_number)
                print(f"{equation} =", result)
                # if we're playing the version where no remainders are allowed, check that
                if no_remainders_allowed:
                    condition = len(my_game.field) == 1
                else:
                    condition = True
                if my_game.won and condition:
                    print("CONGRATULATIONS! You win!")
                    # print("Target:", my_game.target)
                    if len(my_game.field) > 1:
                        s = "Remaining digit"
                        if len(my_game.field) > 2:
                            s += "s"
                        my_game.field.remove(my_game.target)
                        print(f"{s}: {my_game.field}")
                    print(my_game.history_string())
                    exit(0)
                if len(my_game.field) == 1:
                    # we only have one number left, but it's not the target
                    print("LOOOOOSER!! HAHAHA!!!")
                    print(my_game)
                    print(my_game.history_string())
                    exit(0)
            except DigitsError as e:
                print(e.message)
        except ValueError:
            print(f"{equation} is incorrectly formatted. Try again, with an integer,"
                  f" a space, +,-,x, or /, a space, and an integer ")
        except DigitsError as e:
            print("Try again,", e.message)
        except IndexError:
            print("make sure you have three elements, separated by spaces, e.g. 1 + 2")


if __name__ == '__main__':

    # maximum starter: no starters higher than this
    # maximum intermediate result: the "official" solution never goes above this during calculation
    # maximum small starter: three of the six starters don't even go above this
    created_game = generate_game_without_one_step_solution(maximum_starter=25,
                                                           maximum_intermediate_result=1000,
                                                           maximum_small_starter=10,
                                                           max_target=500)
    # A real NYTimes game, level 2
    # my_game = Game(106, [2,5,7,10,11,25])

    # no_remainders_allowed set to True means we have to use up all the digits
    run_game(created_game, no_remainders_allowed=True)                    # in this version, you win even if you have more digits remaining








