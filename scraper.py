import requests
from pprint import pprint
from contextlib import suppress

from bs4 import BeautifulSoup


class WordClass:
    name = ""
    prefix = ""

    @classmethod
    def from_str(cls, name):
        for subcls in cls.__subclasses__():
            if subcls.name == name:
                return subcls()

        raise ValueError(f"Invalid word class: {name}")

    @classmethod
    def __str__(cls):
        return cls.prefix + cls.name


class Noun(WordClass):
    name = "n"
    prefix = "\033[1;32m"


class TransitiveVerb(WordClass):
    name = "vt"
    prefix = "\033[1;33m"


class IntransitiveVerb(WordClass):
    name = "vi"
    prefix = "\033[1;34m"


class Interjection(WordClass):
    name = "interj"
    prefix = "\033[1;35m"


class Modifier(WordClass):
    name = "mod"
    prefix = "\033[1;36m"


class Conjunction(WordClass):
    name = "conj"
    prefix = "\033[1;37m"


class Separator(WordClass):
    name = "sep"
    prefix = "\033[1;38m"


class Definition:
    def __init__(self, word):
        self.word = word
        self.meanings = []

    def add_definition(self, wclass=Noun(), meaning=""):
        self.meanings.append((wclass, meaning))

    def __str__(self):
        res = ""
        meanings = self.meanings.__iter__()
        meaning = next(meanings)

        res += "\033[1m" + self.word + "\033[0m\t"
        res += "\033[3m" + str(meaning[0]) + "\t" + meaning[1] + "\033[0m"

        for meaning in meanings:
            res += "\n"
            res += " " * len(self.word) + "\t"
            res += "\033[3m" + str(meaning[0]) + "\t" + meaning[1] + "\033[0m"

        return res

    def __bool__(self):
        return bool(self.meanings)


def download(url):
    while True:
        with suppress(requests.exceptions.ConnectionError):
            return requests.get(url).content


def get_definitions():
    url = "http://www.tokipona.net/tp/classicwordlist.aspx"
    soup = BeautifulSoup(download(url), "html.parser")

    dls = soup.find_all("dl")

    for dl in dls:
        dt = dl.find("dt")
        term = str(dt.contents[-1]).split()[0].strip(",")

        definition = Definition(term)

        dds = dl.find_all("dd", lang="en")

        for dd in dds:
            if next(dd.children).name != "i":
                break

            try:
                definition.add_definition(
                    WordClass.from_str(dd.contents[0].contents[0]),
                    dd.contents[1].strip()
                )
            except ValueError:
                continue

        if not definition:
            continue

        yield definition


def main():
    for definition in get_definitions():
        print(definition.prettify())
        print()


if __name__ == "__main__":
    main()
