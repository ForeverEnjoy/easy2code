import re

def camelcase(string):
    """
    Demo:
        foo_bar_baz => fooBarBaz
        FooBarBaz => fooBarBaz
    """

    string = re.sub(r"^[\-_\.]", '', str(string))
    if not string:
        return string
    return lowercase(string[0]) + re.sub(r"[\-_\.\s]([a-z])", lambda matched: uppercase(matched.group(1)), string[1:])


def pascalcase(string):
    return capitalcase(camelcase(string))


def capitalcase(string):
    string = str(string)
    if not string:
        return string
    return uppercase(string[0]) + string[1:]


def constcase(string):
    """Convert string into upper snake case.
    Join punctuation with underscore and convert letters into uppercase.
    """
    return uppercase(snakecase(string))


def pathcase(string):
    string = snakecase(string)
    if not string:
        return string
    return re.sub(r"_", "/", string)


def snakecase(string):

    string = re.sub(r"[\-\.\s]", '_', str(string))
    if not string:
        return string
    return lowercase(string[0]) + re.sub(r"[A-Z]", lambda matched: '_' + lowercase(matched.group(0)), string[1:])


def spinalcase(string):
    return re.sub(r"_", "-", snakecase(string))


def uppercase(string):
    return str(string).upper()


def lowercase(string):
    return str(string).lower()

