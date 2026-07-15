from pathlib import Path


def file_has_line(filepath: Path, line: str) -> bool:
    """
    Check if file has given line
    """
    with open(filepath) as f:
        file_lines = [l.rstrip() for l in f.readlines()]
    ret = line in file_lines
    return ret


def add_new_line_to_file(filepath: Path, line: str, prepend: bool = False):
    """
    Add line to given file if it does not contain it.
    """
    if not file_has_line(filepath, line):
        add_line_to_file(filepath, line, prepend)


def add_line_to_file(filepath: Path, line: str, prepend: bool):
    """
    Add line to given file.

    filepath (Path): path to file
    line (str): line to add
    prepend (bool): add to top of file instead of bottom
    """
    with open(filepath) as f:
        lines = f.readlines()
    new_line = f"{line}\n"
    updated_lines = [new_line] + lines if prepend else lines + [new_line]

    with open(filepath, "w") as f:
        f.writelines(updated_lines)
