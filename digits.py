"""
Digits game by Doug and Meaghan

Based on NYTimes Digits game

The player is given 6 natural numbers (n > 0) and a seventh, which is the goal. We have +,-,x,/.
We must stay within N (Natural numbers) at every step.
We need to get the goal with any combinations of the given numbers using the operations.

TODO Possible variants:

    - Must use all digits
    - More operations allowed (square, square root?)
    - Use all of R (Reals: negatives, fractions, square roots...) or Q or at least Z
    - Larger solution space (Z? Q? R?)
    - Different number of starting digits
    - Unique solution
    - give countdown from target (Doug will explain)

Definitions:
    - target (the number we want to get to)
    - starters (the initial 6 numbers)
    - field (the set of current numbers)

DONE Create a game with a solution (the target and starters)

TODO GUI (ask Soren?)

"""
import random
from copy import copy


class DigitsError(Exception):
    def __init__(self, message="Error in game"):
        self.message = message
        super().__init__(self.message)


class Game:
    """
    The state of the game after 0 or more steps

    Attributes:
        target: the number the player wants to reach
        field: the current numbers (initialised to the 6 starters)
    """

    def __init__(self, target, field: list[int]):
        self.target = target
        self.starters = copy(field)
        self.field = field
        self.operations = ["+", "-", "x", "/"]
        self.won = self.target in self.field
        self.history = [copy(self.field)]

    def __repr__(self):
        s = ""
        s += f"operations allowed:"
        for operation in self.operations:
            s = s + f" {operation}"
        # s += "\nHistory"
        # for state in self.history:
        #     s += f"\n{state}"
        s += f"\ntarget: {self.target}"
        s += f"\navailable numbers: {self.field}"
        return s

    def get_operation_from_string(self, operation_as_string):
        if operation_as_string == "+":
            return int.__add__
        elif operation_as_string == "-":
            return int.__sub__
        elif operation_as_string in ["x", "*"]:
            return int.__mul__
        elif operation_as_string == "/":
            return int.__divmod__
        else:
            raise ValueError(f"Operation must be one of {self.operations}")

    def calculate_result(self, first_input: int, operation_as_string: str, second_input: int):
        """
        given the two numbers and operation, calculates the result of applying the operation
        :param first_input: int e.g. 1
        :param operation_as_string: string: needs to be +, -, x, or /, e.g. "+"
        :param second_input: int e.g. 2
        :return: int e.g. 3
        """
        if operation_as_string == "+":
            return first_input + second_input
        elif operation_as_string == "-":
            result = first_input - second_input
            if result < 1:
                raise DigitsError("negative numbers are not allowed")
            return result
        elif operation_as_string in ["x", "*", "X"]:
            return first_input * second_input
        elif operation_as_string == "/":
            dividend, remainder = int.__divmod__(first_input, second_input)
            if remainder > 0:
                raise DigitsError(f"{first_input} cannot be evenly divided by {second_input}")
            else:
                return dividend
        else:
            raise DigitsError(f"Operation must be one of {self.operations}")

    def are_valid_inputs(self, number_1, number_2):
        """
        Checks if the inputs are in the field.
        :param number_2: int: the second input from the user
        :param number_1: int: the first inputs number from the user.
        :return: bool
        """
        if number_1 == number_2:
            return self.field.count(number_1) > 1
        else:
            return number_1 in self.field and number_2 in self.field

    def take_step(self, first_number: int, operation_as_string: str, second_number: int):
        """
        Given inputs from the user, update the game.
            Apply the operation and replace the two operands with the result.
        :param first_number: int: first user input
        :param operation_as_string: +,-,x, or /
        :param second_number: third user input
        :return: the result of apply the operation (just for printing purposes
        """
        if not self.are_valid_inputs(first_number, second_number):
            raise DigitsError(f"{first_number} and/or {second_number} not available")

        result = self.calculate_result(first_number, operation_as_string, second_number)

        # remove the inputs from the field and add the result of the operation
        self.field.remove(first_number)
        self.field.remove(second_number)
        self.field.append(result)

        # did we win?
        self.check_success()

        self.history.append(copy(self.field))

        return result

    def check_success(self):
        """
        updates self.won
        :return:
        """
        won = self.target in self.field
        self.won = won
        return won

    def undo(self):
        if len(self.history) > 1:
            self.history.pop(-1)
            self.field = self.history[-1]
        else:
            print("Nothing to undo")


def create_random_game(maximum_starter=25, maximum_intermediate_result=200, maximum_small_starter=10):
    """
    Create a game
    :param maximum_small_starter: half the starting digits are no bigger than this (default 10)
    :param maximum_intermediate_result: the gold solution never has an intermediate result higher than this (default 200)
    :param maximum_starter: starter digits can't be larger than this (default 25)
    :return: Game
    """
    starters = random.sample(range(1, maximum_small_starter), k=3)
    starters += random.sample([i for i in range(1, maximum_starter) if i not in starters], k=3)
    game = Game(0, starters)
    while len(game.field) > 1:
        # print(game)
        op = random.choice(game.operations)
        numbers = random.sample(game.field, k=2)
        try:
            result = game.calculate_result(numbers[0], op, numbers[1])
        except DigitsError as e:
            # print(e)
            continue
        if result > maximum_intermediate_result:
            continue
        print(game)
        print(f"{numbers[0]} {op} {numbers[1]}")
        game.take_step(numbers[0], op, numbers[1])
        game.target = result
    return Game(game.target, game.starters)


def run_game(my_game: Game, max_steps=None):
    """
    User interface.
    Uses input to interact with player.
    Inputs required to be separated by white space, as in 1 + 2
    :param max_steps: Stop after this many steps. Default 1000000000
    :param my_game: an initialised Game
    """
    if max_steps is None:
        max_steps = 1000000000
    step = 0
    while step < max_steps:
    # while False:
        step += 1
        print()
        print("input example: 1 + 2")
        print("To stop the game, type 'exit'")
        print("To undo, type 'undo'")
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
                if my_game.won:
                    print("CONGRATULATIONS! You win!")
                    print("Target:", my_game.target)
                    if len(my_game.field) > 1:
                        s = "Remaining digit"
                        if len(my_game.field) > 2:
                            s += "s"
                        my_game.field.remove(my_game.target)
                        print(f"{s}: {my_game.field}")
                    exit(0)
                if len(my_game.field) == 1:
                    # we only have one number left, but it's not the target
                    print("LOOOOOSER!! HAHAHA!!!")
                    exit(0)
                print("History:")
                for state in my_game.history:
                    print(state)
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

    created_game = create_random_game()
    # A real NYTimes game, level 2
    # my_game = GameState(106, [2,5,7,10,11,25])

    run_game(created_game)







