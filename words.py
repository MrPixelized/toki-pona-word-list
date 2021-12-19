class WordClass:
    name = None
    prefix = None

    def __new__(cls, name=None):
        if cls != WordClass:
            return super(WordClass, cls).__new__(cls)

        if name is None:
            return cls()

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

        res += "\033[1m" + self.word + "\033[0m\t"

        for meaning in meanings:
            res += "\033[3m" + str(meaning[0]) + "\033[0m\t"
            res += meaning[0].prefix + meaning[1] + "\033[0m"
            res += "\n"
            res += " " * len(self.word) + "\t"

        return "\n".join(res.split("\n")[:-1])

    def __bool__(self):
        return bool(self.meanings)
