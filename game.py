from copy import copy


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
        # s += self.operations_string()
        # s += self.history_string()
        s += f"\ntarget: {self.target}"
        s += f"\navailable numbers: {self.field}"
        return s

    def operations_string(self):
        s = "operations allowed:"
        for operation in self.operations:
            s = s + f" {operation}"
        return s

    def history_string(self):
        s = "\nHistory"
        for state in self.history:
            s += f"\n{state}"
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


class DigitsError(Exception):
    def __init__(self, message="Error in game"):
        self.message = message
        super().__init__(self.message)
