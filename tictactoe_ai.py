import random
from typing import Any

GAME_SYMBOLS: set[str] = {"X", "O", "_"}
STARTING_TABLE_LEN: int = 9


class WrongCoordinates(ValueError):
    pass


def game_table(input_matrix: list[list[str]]) -> str:
    """
    Prints the game's table.
    :param input_matrix: A game matrix with current state of game.
    :return: The game's table.
    """

    return (f"""
    ---------
    | {input_matrix[0][0]} {input_matrix[0][1]} {input_matrix[0][2]} |
    | {input_matrix[1][0]} {input_matrix[1][1]} {input_matrix[1][2]} |
    | {input_matrix[2][0]} {input_matrix[2][1]} {input_matrix[2][2]} |
    ---------
    """)


def get_a_winning_row_and_symbol(matrix: list[Any]) -> tuple:
    """
    Checks whether there are only one type of symbols: 'X' or 'O' in a row or whether the row is not empty.
    :param matrix: A game matrix with current state of game.
    :return: A number of winning rows and a winning symbol.
    """

    number_of_winning_rows: int = 0
    winning_symbol: str = ""
    for row in matrix:
        if len(set(row)) == 1 and set(row) != {" "}:
            number_of_winning_rows += 1
            winning_symbol = row[0]
    return number_of_winning_rows, winning_symbol


def split_and_validate_coordinates(coordinates: str) -> tuple[int, int]:
    try:
        y, x = coordinates.split()
    except ValueError:
        raise WrongCoordinates("You should enter numbers!")

    if x.isnumeric() and y.isnumeric():
        x = int(x)
        y = int(y)
    else:
        raise WrongCoordinates("You should enter numbers!")

    if x not in (1, 2, 3) or y not in (1, 2, 3):
        raise WrongCoordinates("Coordinates should be from 1 to 3!")
    return y, x


def search_possible_move_coordinates(matrix: list[list[str]]) -> list[tuple[int, int]]:
    empty_cells_coordinates: list[tuple[int, int]] = []
    for x_index, line in enumerate(matrix):
        for y_index, cell in enumerate(line):
            if cell == " ":
                empty_cells_coordinates.append((y_index + 1, x_index + 1))
    return empty_cells_coordinates


def check_game_result(matrix: list[list[str]]) -> str:
    x_quantity: int = 0
    o_quantity: int = 0
    empty_cell_quantity: int = 0

    # rotates (transposes) the matrix for easier iterations through columns with for loops
    matrix_transposed: list[tuple[Any]] = list(zip(*matrix))

    # contains the diagonals of the game matrix
    matrix_diagonals: list[list[str]] = [
        [matrix[0][0], matrix[1][1], matrix[2][2]],
        [matrix[0][2], matrix[1][1], matrix[2][0]]
    ]

    winning_rows, winning_row_symbol = get_a_winning_row_and_symbol(matrix)

    winning_columns, winning_column_symbol = get_a_winning_row_and_symbol(matrix_transposed)

    winning_diagonals, winning_diagonal_symbol = get_a_winning_row_and_symbol(matrix_diagonals)

    for line in matrix:
        x_quantity += line.count("X")
        o_quantity += line.count("O")
        empty_cell_quantity += line.count(" ")

    # checks whether there aren't too many symbols of one type or more than one winning rows
    if abs(x_quantity - o_quantity) > 1 or winning_rows > 1 or winning_columns > 1:
        whose_turn.reverse()
        return "Impossible"
    elif winning_rows == 0 and winning_columns == 0 and winning_diagonals == 0 and empty_cell_quantity == 0:
        return "Draw"

    if winning_rows == 1:
        return f"{winning_row_symbol} wins"
    elif winning_columns == 1:
        return f"{winning_column_symbol} wins"
    elif winning_diagonals == 1:
        return f"{winning_diagonal_symbol} wins"
    elif empty_cell_quantity > 0:
        return ""


if __name__ == '__main__':
    whose_turn: list = ["X", "O"]

    game_matrix: list[list[str]] = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

    print(game_table(game_matrix))

    while True:
        while True:
            possible_moves = search_possible_move_coordinates(game_matrix)
            if whose_turn[0] == "X":
                move_coordinates: str = input("Enter the coordinates: ")
                try:
                    y, x = split_and_validate_coordinates(move_coordinates)
                except WrongCoordinates as error:
                    print(error)
                    continue
            else:
                y, x = random.choice(possible_moves)
                print('Making move level "easy"')

            if (y, x) not in possible_moves:
                print("This cell is occupied! Choose another one!")
            else:
                game_matrix[y - 1][x - 1] = whose_turn[0]
                print(game_table(game_matrix))
                break

        game_result = check_game_result(game_matrix)

        if game_result:
            print(game_result)
            break
        else:
            whose_turn.reverse()
