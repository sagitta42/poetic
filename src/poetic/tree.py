from pathlib import Path

space = "    "
branch = "│   "
tee = "├── "
final = "└── "


def tree(path: Path, prefix: str = ""):
    """
    Display directory tree akin to bash tree.

    A recursive generator, given a directory Path object
        will yield a visual tree structure akin to that of bash/GNU tree

    https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    """
    contents = list(path.iterdir())
    pointers = [tee] * (len(contents) - 1) + [final]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir() and not path.name in ["venv", ".git", "poetry.lock"]:
            extension = branch if pointer == tee else space
            yield from tree(path, prefix=prefix + extension)
