import random
import sys

WORDS: list = ['python', 'java', 'kotlin', 'javascript']


def menu() -> None:
    while True:
        choice: str = input("Type \"play\" to play the game, \"exit\" to quit:")
        if choice == "play":
            break
        elif choice == "exit":
            sys.exit()


def game(number_of_tries: int = 8) -> None:
    print("H A N G M A N")

    word_to_guess: str = random.choice(WORDS)
    hint: str = "-" * len(word_to_guess)
    guessed_letters: set = set()

    while number_of_tries > 0:
        print()
        print(hint)
        guess: str = input(f"Input a letter: ")

        if len(guess) != 1:
            print("You should input a single letter")
            continue

        if guess.isupper() or not guess.isalpha():
            print("Please enter a lowercase English letter")
            continue

        if guess in guessed_letters:
            print("You've already guessed this letter")
            continue

        if guess in word_to_guess:
            for index, letter in enumerate(word_to_guess):
                if guess == letter:
                    hint: list = list(hint)
                    hint[index] = guess
                    hint = "".join(hint)
        else:
            print("That letter doesn't appear in the word")
            number_of_tries -= 1

        guessed_letters.add(guess)

        if hint == word_to_guess:
            print()
            print(word_to_guess)
            print("You guessed the word!")
            print("You survived!")
            break

    if hint != word_to_guess:
        print("You lost!")


if __name__ == '__main__':
    while True:
        menu()
        game(number_of_tries=8)
