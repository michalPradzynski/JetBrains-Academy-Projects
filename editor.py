"""
This script helps to convert your text into markdown formatted text 
that can be used in for example README.md files.
Simply specify which formatter you want to use, choose additional options and type in your text.
In the end, the whole provided lines are saved into 'output.md' file.
"""

FORMATTERS: list = ["plain", "bold", "italic", "link", "inline-code", "header", "new-line", "ordered-list", "unordered-list"]
SPECIAL_COMMANDS: list = ["!help", "!done"]


def text(command: str) -> str:
    input_text: str = input("- Text: ")
    text_options: dict = {
        "plain": input_text,
        "bold": f"**{input_text}**",
        "italic": f"*{input_text}*",
        "inline-code": f"`{input_text}`"
    }
    return text_options[command]


def link() -> str:
    label: str = input("- Label: ")
    url: str = input("- URL: ")
    link_text: str = f"[{label}]({url})"
    return link_text


def header() -> str:
    while True:
        header_level: int = int(input("- Level: "))
        if header_level not in range(1, 7):
            print("The level should be within the range of 1 to 6")
        else:
            break
    input_text: str = input("- Text: ")
    header_text: str = header_level * "#" + " " + input_text + "\n"
    return header_text


def listing(command: str) -> list:
    while True:
        rows_number: int = int(input("Number of rows: "))
        if rows_number <= 0:
            print("The number of rows should be greater than zero")
        else:
            break
    whole_list: list = []
    for row_index in range(1, rows_number + 1):
        row_text: str = input(f"Row #{row_index}: ")
        if command == "ordered-list":
            whole_list.append(f"{row_index}. {row_text}\n")
        elif command == "unordered-list":
            whole_list.append(f"* {row_text}\n")
    return whole_list


def help_menu() -> None:
    print("Available formatters:", end="")
    for formatter in FORMATTERS:
        print(f" {formatter}", end="")
    print()
    print("Special commands:", end="")
    for special in SPECIAL_COMMANDS:
        print(f" {special}", end="")
    print()


def save_to_file(input_text: list) -> None:
    with open("output.md", "w") as file:
        file.writelines(input_text)


def main():
    markdown_text: list = []

    while True:
        command: str = input("- Choose a formatter: ")

        if command not in (FORMATTERS + SPECIAL_COMMANDS):
            print("Unknown formatting type or command. Please try again")
        elif command == "!help":
            help_menu()
        elif command == "!done":
            save_to_file(markdown_text)
            break

        if command == "header":
            markdown_text.append(header())
        elif command == "link":
            markdown_text.append(link())
        elif command == "new-line":
            markdown_text.append("\n")
        elif command in ("ordered-list", "unordered-list"):
            output_list: list = listing(command)
            for row in output_list:
                markdown_text.append(row)
        else:
            markdown_text.append(text(command))

        print("".join(markdown_text))


if __name__ == '__main__':
    main()
