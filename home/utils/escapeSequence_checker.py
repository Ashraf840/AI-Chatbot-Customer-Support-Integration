import re

def searcEscapeSequence(str):
    first_search = re.search("\n", str)
    return True if first_search is not None else False
