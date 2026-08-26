import os
from pathlib import Path


class PathUtil:
    def __init__(self, path: Path) -> None:
        self._path = path


class Dir(PathUtil):
    def exists_and_non_empty(self) -> bool:
        """
        Check if path exists and is not empty
        """
        ret = self._path.exists() and len(os.listdir(self._path)) > 0
        return ret


class File(PathUtil):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self._lines = []
        if self._path.exists():
            with open(self._path) as f:
                self._lines = [l.rstrip() for l in f.readlines()]

    def add_new_line(self, line: str, prepend: bool = False):
        """
        Add line to file if it does not contain it.
        """
        if not self._has_line(line):
            self._add_line(line, prepend)

    def remove_line(self, line: str):
        """
        Remove all instances of line in file.
        """
        pass

    def replace_str(self, str_original: str, str_replace: str):
        """
        Replace given string with another in file.

        Replaces all instances of given string.
        """
        new_lines = [line.replace(str_original, str_replace) for line in self._lines]
        self._write(new_lines)

    def _has_line(self, line: str) -> bool:
        """
        Check if file has given line
        """
        ret = line.rstrip() in self._lines
        return ret

    def _add_line(self, line: str, prepend: bool):
        """
        Add line to file.

        prepend (bool): add to top of file instead of bottom
        """
        new_line = f"{line}"
        updated_lines = (
            [new_line] + self._lines if prepend else self._lines + [new_line]
        )
        self._write(updated_lines)

    def _write(self, lines: list[str]):
        """
        Write given lines to file.

        Expects lines without the end of line characters.
        """
        with open(self._path, "w") as f:
            f.writelines([f"{l}\n" for l in lines])
