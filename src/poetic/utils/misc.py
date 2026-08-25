from typing import Iterable

POETIC_LINK = "[poetic](https://github.com/sagitta42/poetic)"


def list_as_args(lst: Iterable) -> str:
    """
    Transform list into a list of command line arguments.

    Example:
    >>> list_as_args(["install", "--no-root"])
    "install --no-root"
    """
    return " ".join(str(element) for element in lst)


