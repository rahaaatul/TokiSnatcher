from os import name, system

import questionary

from .chapters import get_chapters
from .download import get_input
from .search import search_book

cls = lambda: system("cls" if name == "nt" else "clear")

choices = ["Search book", "Download from URL", "Exit"]


def main():
    selected_action = questionary.select("Choose action:", choices=choices).ask()

    options = [search_book, get_input, exit]
    res = options[choices.index(selected_action)]()

    if res:
        cls()
        get_chapters(res)


if __name__ == "__main__":
    main()
