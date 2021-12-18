import requests
from pprint import pprint
from contextlib import suppress

from bs4 import BeautifulSoup


class Definition:
    def __init__(self, word):
        self.word = word
        self.meanings = []

    def add_definition(self, wclass="n", meaning=""):
        self.meanings.append((wclass, meaning))

    def __str__(self):
        res = ""
        after = "\t"
        meanings = self.meanings.__iter__()

        res += self.word + after + ": \t".join(next(meanings))

        for meaning in meanings:
            res += "\n" + " " * len(self.word) + after + ": \t".join(meaning)

        return res

    def __bool__(self):
        return bool(self.meanings)


def download(url):
    while True:
        with suppress(requests.exceptions.ConnectionError):
            return requests.get(url).content


def main():
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

            definition.add_definition(
                dd.contents[0].contents[0],
                dd.contents[1].strip()
            )

        if not definition:
            continue

        print(definition)
        print()


if __name__ == "__main__":
    main()
