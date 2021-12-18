from os import system
from random import randint, shuffle
from readchar import readchar

from scraper import get_definitions


class Card:
    def __init__(self, obj):
        self.known = False
        self.tries = 0

        self.knowledge = obj

    def flip(self):
        print(self.knowledge.prettify())
        print()

        ans = None
        while ans not in ("y", "n", "q"):
            print("Known? (y/n/q)")
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
        print(f"({total - len(cards)} / {total})")
        print()

        card = cards.pop()
        card.flip()

        pos = len(cards) - randint(0, round(len(cards) * 0.1))

        if not card.known:
            cards.insert(pos, card)
        elif card.tries > 0:
            card.ties -= 2
            cards.insert(pos, card)


if __name__ == "__main__":
    main()
