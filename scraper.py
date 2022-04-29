import requests
from contextlib import suppress

from bs4 import BeautifulSoup, NavigableString

from words import WordClass, Definition, PhraseDefinition


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


def get_omniglot_phrases():
    url = "https://omniglot.com/language/phrases/tokipona.htm"
    soup = BeautifulSoup(download(url), "html.parser")

    trs = iter(soup.select("div#unicode table tbody tr"))
    try:
        next(trs)
    except StopIteration:
        return

    for tr in trs:
        for elem in tr(["em"]):
            elem.replace_with_children()

        tds = tr.select("td")

        # English phrase
        if link := tds[0].select_one("a"):
            phrase = link.contents[0] + "".join(map(str, tds[0].contents[1:]))
        else:
            phrase = tds[0].contents[0]
        definition = PhraseDefinition(phrase)

        meaning = []
        # Toki pona phrases
        for elem in tds[1]:
            if elem.name == "br":
                definition.add_definition(" ".join(meaning).strip())
                meaning = []
                continue

            try:
                meaning.append(elem.contents[0].strip())
            except AttributeError:
                meaning.append(str(elem).strip())
        else:
            definition.add_definition(" ".join(meaning).strip())

        yield definition


def main():
    for phrase in get_omniglot_phrases():
        print(phrase)
        print()

    return
    for definition in get_definitions():
        print(definition)
        print()


if __name__ == "__main__":
    main()
