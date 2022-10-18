# this file contains functions which change the style and colour of the output

def pprint(*args, spaces: bool=False) -> str:
    """
    Returns a string of strings/numbers which are divided with spaces, commas 
    and the word "and".
    """
    string = str()
    for i, arg in enumerate(args):
        if i != 0:
            string += " " if spaces else ", " if i+1 < len(args) else " and "
        string += str(arg)
    return string


def NORM(*args) -> str:
    """
    Resets all the style and color settings
    """
    return "\033[0m" + pprint(*args, spaces=True)


def BOLD(*args) -> str:
    """
    Returns given arguments seperated by spaces and bold 
    """
    return "\033[1m" + pprint(*args, spaces=True) + "\033[22m"


def DIM(*args) -> str:
    """
    Returns given arguments seperated by spaces and dimmed 
    """
    return "\033[2m" + pprint(*args, spaces=True) + "\033[22m"


def ITAL(*args) -> str:
    """
    Returns given arguments seperated by spaces and italic 
    """
    return "\033[3m" + pprint(*args, spaces=True) + "\033[23m"


def UNDL(*args) -> str:
    """
    Returns given arguments seperated by spaces and underlined 
    """
    return "\033[4m" + pprint(*args, spaces=True) + "\033[24m"


def STRIKE(*args) -> str:
    """
    Returns given arguments seperated by spaces and striked 
    """
    return "\033[9m" + pprint(*args, spaces=True) + "\033[29m"


def RED(*args) -> str:
    """
    Returns given arguments seperated by spaces and in red 
    """
    return "\033[31m" + pprint(*args, spaces=True) + "\033[39m"


def GREEN(*args) -> str:
    """
    Returns given arguments seperated by spaces and in green 
    """
    return "\033[32m" + pprint(*args, spaces=True) + "\033[39m"


def YELLOW(*args) -> str:
    """
    Returns given arguments seperated by spaces and in yellow 
    """
    return "\033[33m" + pprint(*args, spaces=True) + "\033[39m"


def BLUE(*args) -> str:
    """
    Returns given arguments seperated by spaces and in blue 
    """
    return "\033[34m" + pprint(*args, spaces=True) + "\033[39m"
