from typing import Any

GAME_SYMBOLS: set[str] = {"X", "O", "_"}
STARTING_TABLE_LEN: int = 9


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


def is_there_a_winning_row(matrix: list[Any]) -> tuple:
    """
    Checks whether there are only one type of symbols: 'X' or 'O' in a row or the row is not empty.
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


if __name__ == '__main__':
    global X_quantity
    global O_quantity
    global empty_cell_quantity
    whose_turn: list = ["X", "O"]

    game_matrix: list[list[str]] = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    while True:
        starting_table: str = input("Please enter starting table: ")
        if len(starting_table) != STARTING_TABLE_LEN:
            print("Wrong length of the starting table!")
            continue
        elif set(starting_table) != GAME_SYMBOLS:
            print("Wrong symbols in the starting table!")
            continue
        else:
            # splitting string into a 3x3 matrix
            starting_table = starting_table.replace("_", " ")
            game_matrix = [list(starting_table[x:x+3]) for x in range(0, len(starting_table), 3)]
            print(game_table(game_matrix))
            break

    while True:
        while True:
            move_coordinates: str = input("Please enter coordinates of your move (row column): ")
            try:
                y, x = move_coordinates.split()
            except ValueError:
                print("You should enter numbers!")
                continue

            if x.isnumeric() and y.isnumeric():
                x = int(x)
                y = int(y)
            else:
                print("You should enter numbers!")
                continue

            if x not in (1, 2, 3) or y not in (1, 2, 3):
                print("Coordinates should be from 1 to 3!")
                continue

            if game_matrix[y - 1][x - 1] == "X" or game_matrix[y - 1][x - 1] == "O":
                print("This cell is occupied! Choose another one!")
            else:
                X_quantity: int = 0
                O_quantity: int = 0
                empty_cell_quantity: int = 0

                for line in game_matrix:
                    X_quantity += line.count("X")
                    O_quantity += line.count("O")
                    empty_cell_quantity += line.count(" ")

                if X_quantity > O_quantity:
                    whose_turn.reverse()

                game_matrix[y - 1][x - 1] = whose_turn[0]
                print(game_table(game_matrix))
                break

        # rotates (transposes) the matrix for easier iterations through columns with for loops
        game_matrix_transposed: list[tuple[Any]] = list(zip(*game_matrix))

        # contains the diagonals of the game matrix
        game_matrix_diagonals: list[list[str]] = [
            [game_matrix[0][0], game_matrix[1][1], game_matrix[2][2]],
            [game_matrix[0][2], game_matrix[1][1], game_matrix[2][0]]
        ]

        winning_rows, winning_row_symbol = is_there_a_winning_row(game_matrix)

        winning_columns, winning_column_symbol = is_there_a_winning_row(game_matrix_transposed)

        winning_diagonals, winning_diagonal_symbol = is_there_a_winning_row(game_matrix_diagonals)

        # checks whether there aren't too many symbols of one type or more than one winning rows
        if abs(X_quantity - O_quantity) > 1 or winning_rows > 1 or winning_columns > 1:
            print("Impossible")
            whose_turn.reverse()
            break
        elif winning_rows == 0 and winning_columns == 0 and winning_diagonals == 0 and empty_cell_quantity == 0:
            print("Draw")
            break

        if winning_rows == 1:
            print(f"{winning_row_symbol} wins")
            break
        elif winning_columns == 1:
            print(f"{winning_column_symbol} wins")
            break
        elif winning_diagonals == 1:
            print(f"{winning_diagonal_symbol} wins")
            break
        elif empty_cell_quantity > 0:
            print("Game not finished")

        whose_turn.reverse()
