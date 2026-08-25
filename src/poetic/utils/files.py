from pathlib import Path


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
