import requests
from contextlib import suppress

from words import WordClass, Definition
from bs4 import BeautifulSoup


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
                    WordClass(dd.contents[0].contents[0]),
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
