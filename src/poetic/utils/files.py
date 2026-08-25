from pathlib import Path


def file_has_line(filepath: Path, line: str) -> bool:
    """
    Check if file has given line
    """
    with open(filepath) as f:
        file_lines = [l.rstrip() for l in f.readlines()]
    ret = line.rstrip() in file_lines
    return ret


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


def add_new_line_to_file(filepath: Path, line: str, prepend: bool = False):
    """
    Add line to given file if it does not contain it.
    """
    if not file_has_line(filepath, line):
        add_line_to_file(filepath, line, prepend)


def replace_str_in_file(str_original: str, str_replace: str, filepath: Path):
    """
    Replace given string with another in filepath.

    Replaces all instances of given string.
    Writes updated lines into same filepath.
    """
    with open(filepath) as f:
        source_file_lines = f.readlines()

    source_file_lines = [
        line.replace(str_original, str_replace) for line in source_file_lines
    ]

    with open(filepath, "w") as f:
        f.writelines(source_file_lines)


def path_exists_non_empty(path: Path) -> bool:
    """
    Check if path exists and is not empty
    """
    ret = path.exists() and len(os.listdir(path)) > 0
    return ret
