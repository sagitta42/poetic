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


def dict_as_args(dct: dict) -> str:
    return " ".join(f"{key}={value}" for key, value in dct.items())


def find_line(lines: list[str], line: str) -> int | None:
    """
    Find line among lines.

    Return index in list or null if not found.
    """
    for idx, l in enumerate(lines):
        if l.strip() == line.strip():
            return idx

    return None


def find_line_startswith(lines: list[str], startswith: str) -> str | None:
    """
    Find line that starts with or null if not found.
    """
    for l in lines:
        if l.lstrip().startswith(startswith):
            return l
    return None
