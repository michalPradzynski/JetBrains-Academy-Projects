"""
This script is a math quiz which tests your skills in either solving
random simple math equations or calculating square roots of random int numbers from 11 to 29.
"""

import sys
from random import randint, choice
from typing import Union

SYMBOLS = ("+", "-", "*")
LEVELS: dict = {
    1: "simple operations with numbers 2-9",
    2: "integral squares 11-29"
}


def add(x: int, y: int) -> int:
    return x + y


def subtract(x: int, y: int) -> int:
    return x - y


def multiply(x: int, y: int) -> int:
    return x * y


def random_math_operation() -> str:
    first_number: int = randint(2, 9)
    second_number: int = randint(2, 9)
    symbol: str = choice(SYMBOLS)
    return f"{first_number} {symbol} {second_number}"


def validate_answer() -> int:
    while True:
        user_answer: Union[str, int] = input()
        try:
            assert not user_answer.isspace()
            user_answer = int(user_answer)
        except (AssertionError, ValueError):
            print("Incorrect format")
        else:
            return user_answer


def endgame(mark: int, difficulty: int) -> None:
    end_question: str = input(f"Your mark is {mark}/5. "
                              f"Would you like to save your result to the file? Enter yes or no.")
    if end_question in ("yes", "YES", "y", "Yes", "Y"):
        username: str = input("What's your username? ")
        with open("results.txt", "a+") as file:
            file.write(f"{username}: {mark}/5 in level {difficulty} ({LEVELS[difficulty]})")
            print(f"The results are saved in \"{file.name}\"")
    else:
        sys.exit()


def main():
    mark: int = 0

    while True:
        try:
            difficulty: int = int(input(f"""Which level do you want? Enter a number: 
            1 - {LEVELS[1]}
            2 - {LEVELS[2]}"""))
            assert difficulty in (1, 2)
        except (AssertionError, ValueError):
            print("Incorrect format.")
        else:
            break

    if difficulty == 1:
        for i in range(5):
            equation: str = random_math_operation()
            print(equation)

            first_number, symbol, second_number = equation.split()

            options: dict = {
                "+": add(int(first_number), int(second_number)),
                "-": subtract(int(first_number), int(second_number)),
                "*": multiply(int(first_number), int(second_number))
            }

            user_answer = validate_answer()
            if user_answer == options[symbol]:
                print("Right!")
                mark += 1
            else:
                print("Wrong!")

    elif difficulty == 2:
        for i in range(5):
            number_to_square: int = randint(11, 29)
            print(number_to_square)

            solution: int = number_to_square ** 2

            user_answer = validate_answer()
            if user_answer == solution:
                print("Right!")
                mark += 1
            else:
                print("Wrong!")

    endgame(mark, difficulty)


if __name__ == '__main__':
    main()
