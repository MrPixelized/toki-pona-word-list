import re
from textwrap import indent, fill
from os import system, get_terminal_size
from random import randint, shuffle
from readchar import readchar

from scraper import get_definitions


def replace_tab(s, tabstop=8):
    """ Credit: Samuel on StackOverflow """
    result = str()

    for c in s:
        if c == '\t':
            result += ' '
            while len(result) % tabstop != 0:
                result += ' '
        else:
            result += c

    return result


class Card:
    def __init__(self, obj):
        self.known = False
        self.tries = 0

        self.definition = obj

    def flip(self, infostring=""):
        # Obtain aesthetic variables
        definition = str(self.definition)
        definition = "\n".join(map(replace_tab, definition.split("\n")))

        twidth = get_terminal_size().columns
        theight = get_terminal_size().lines

        width = max(map(len,
            re.sub(r"\\x1b\[.*?m", "", str(definition.encode("ascii")))[2:-1]
            .split("\\n"))
        )
        height = len(definition.split("\n"))

        hpad = (twidth - width) // 2 * " "
        vpad = ((theight - height) // 2 - infostring.count("\n") - 1) * "\n"

        # Print initial prompt
        system("clear")
        print(infostring)
        print(vpad)
        print(f"\033[1m{self.definition.word}\033[0m".center(twidth))
        print()
        print("Flip card...".center(twidth))
        if readchar() == "q":
            raise KeyboardInterrupt

        # Print answer
        system("clear")
        print(infostring)
        print(vpad)
        print(indent(definition, hpad))
        print()
        print("Known? (y/n/q)".center(twidth))

        ans = None
        while ans not in ("y", "n", "q"):
            ans = readchar()

        if ans == "y":
            self.known = True
        elif ans == "n":
            self.tries += 1
        else:
            raise KeyboardInterrupt


def main():
    cards = [Card(definition) for definition in get_definitions()]
    total = len(cards)
    shuffle(cards)

    while cards:
        system("clear")
        card = cards.pop()
        card.flip(infostring=f"({total - len(cards) - 1} / {total})")

        pos = len(cards) - randint(0, round(len(cards) * 0.1))

        if not card.known:
            cards.insert(pos, card)
        elif card.tries > 0:
            card.tries -= 2
            cards.insert(pos, card)


if __name__ == "__main__":
    main()
