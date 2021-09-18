"""
This project uses sqlite3 to manage a simple banking system in which you can create and delete an account
and transfer money between existing accounts. Additionally, in creation of a new bank account and in validation
of input card numbers Luhn Algorithm is being used.
"""

import sqlite3
import sys

from random import randint
from sqlite3 import OperationalError, Cursor
from typing import Union

MENU_PROMPT: str = """
1. Create an account
2. Log into account
0. Exit
"""
ACCOUNT_MENU_PROMPT: str = """
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""

DB_NAME: str = "card.s3db"


def luhn_algorithm(account_number: str) -> int:
    split_number: list
    control_number: int
    checksum: int

    # split given account number to digits and convert them to int
    split_number = [int(digit) for digit in account_number]
    # multiply odd digits by 2
    split_number = [digit * 2 if (index + 1) % 2 != 0 else digit for index, digit in enumerate(split_number)]
    # subtract 9 from numbers over 9
    split_number = [digit - 9 if digit > 9 else digit for digit in split_number]
    # sum all numbers
    control_number = sum(split_number)
    # generate checksum
    checksum = 10 - (control_number % 10)
    return 0 if checksum == 10 else checksum


class Card:
    number: str
    pin: str
    balance: int

    def new_card(self):
        self.number = "400000" + format(randint(0, 999999999), "09d")
        self.number += str(luhn_algorithm(self.number))
        self.pin = format(randint(0, 9999), "04d")
        self.balance = 0

    def __str__(self):
        return f"""
Your card number:
{self.number}
Your card PIN:
{self.pin}"""


class DBConnection:
    def __init__(self):
        self.connection = sqlite3.connect(DB_NAME)
        self.cursor = self.connection.cursor()

    def create_card_table(self) -> None:
        try:
            self.cursor.execute("SELECT * FROM card")
        except OperationalError:
            self.cursor.execute("""CREATE TABLE card (
                id INTEGER,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0
                )""")
            self.connection.commit()

    def insert_into_table(self, columns: Union[str, tuple], values: Union[str, int, tuple]) -> None:
        self.cursor.execute(f"INSERT INTO card {columns} VALUES {values}")
        self.connection.commit()

    def select_from_table(self, columns: str, where: Union[str, None] = None) -> Cursor:
        if where is None:
            return self.cursor.execute(f"SELECT {columns} FROM card")
        else:
            return self.cursor.execute(f"SELECT {columns} FROM card WHERE {where}")

    def delete_from_table(self, where: str) -> None:
        self.cursor.execute(f"DELETE FROM card WHERE {where}")
        self.connection.commit()

    def update_table(self, set_columns: str, where: str) -> None:
        self.cursor.execute(f"UPDATE card SET {set_columns} WHERE {where}")
        self.connection.commit()

    def get_card_balance(self, where: str) -> Cursor:
        return self.cursor.execute(f"SELECT balance FROM card WHERE {where}").fetchone()[0]


def main():
    table_id: int = 0
    menu_choice: int
    wanted_card_number: str
    wanted_card_pin: str

    db = DBConnection()
    db.create_card_table()

    while True:
        menu_choice = int(input(MENU_PROMPT))

        if menu_choice == 1:
            card = Card()
            card.new_card()
            table_id += 1

            db.insert_into_table(columns=("id", "number", "pin", "balance"),
                                 values=(table_id, card.number, card.pin, card.balance))

            print("Your card has been created")
            print(card)

        elif menu_choice == 2:
            wanted_card_number: str
            wanted_card_pin: str
            logged_in_card: Union[None, Card] = None

            wanted_card_number = input("Enter your card number: ")
            wanted_card_pin = input("Enter your PIN: ")

            for _, card_number, card_pin, card_balance in db.cursor.execute("SELECT * FROM card"):
                if wanted_card_number == card_number and wanted_card_pin == card_pin:
                    logged_in_card = Card()
                    logged_in_card.number = card_number
                    logged_in_card.pin = card_pin
                    logged_in_card.balance = card_balance
                    break

            if logged_in_card is None:
                print("Wrong card number or PIN!")

            else:
                print("You have successfully logged in!")
                while True:
                    account_balance: Union[int, Cursor, None]

                    account_balance = db.get_card_balance(where=f"number = '{logged_in_card.number}'")
                    menu_choice = int(input(ACCOUNT_MENU_PROMPT))

                    if menu_choice == 1:
                        print(f"Balance: {account_balance}")

                    elif menu_choice == 2:
                        income: int

                        income = int(input("Enter income: "))
                        account_balance += income
                        db.update_table(set_columns=f"balance = {account_balance}",
                                        where=f"number = '{logged_in_card.number}'")
                        print("Income added!")

                    elif menu_choice == 3:
                        card_number_transfer: str
                        transfer_money: int
                        all_cards_in_db: list

                        all_cards_in_db = [row[0] for row in db.select_from_table(columns="number").fetchall()]

                        card_number_transfer = input("""Transfer
                        Enter card number: """)

                        if card_number_transfer == logged_in_card.number:
                            print("You can't transfer money to the same account!")

                        elif card_number_transfer[-1] != str(luhn_algorithm(card_number_transfer[:-1])):
                            print("Probably you made a mistake in the card number. Please try again!")

                        elif card_number_transfer not in all_cards_in_db:
                            print("Such a card does not exist.")

                        else:
                            transfer_money = int(input("Enter how much money you want to transfer: "))

                            if transfer_money > account_balance:
                                print("Not enough money!")

                            else:
                                account_balance -= transfer_money
                                db.update_table(set_columns=f"balance = {account_balance}",
                                                where=f"number = '{logged_in_card.number}'")

                                account_transferred_to_balance = db.get_card_balance(where=f"number = '{card_number_transfer}'")
                                account_transferred_to_balance += transfer_money
                                db.update_table(set_columns=f"balance = {account_transferred_to_balance}",
                                                where=f"number = '{card_number_transfer}'")

                                print("Success!")

                    elif menu_choice == 4:
                        db.delete_from_table(where=f"number = '{logged_in_card.number}'")
                        print("The account has been closed!")
                        del logged_in_card
                        break

                    elif menu_choice == 5:
                        print("You have successfully logged out!")
                        del logged_in_card
                        break

                    elif menu_choice == 0:
                        print("Bye!")
                        sys.exit()

        elif menu_choice == 0:
            db.connection.close()
            print("Bye!")
            sys.exit()


if __name__ == '__main__':
    main()
