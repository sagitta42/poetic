from pathlib import Path
from typing import Any

from dotenv import set_key

from poetic.logger import logg
from poetic.utils.path import File


class DotEnv:
    def __init__(self, path: Path):
        self._path = path / ".env.template"

    @property
    def file(self) -> File:
        return File(self._path)

    def set(self, name: str, value: Any, comment: bool = False):
        """
        Update .env variable or add commented value.
        """
        update_method = self.commented_var if comment else self.set_var
        update_method(name, value)

    def set_var(self, name: str, value: Any):
        """
        Update env variable.
        """
        set_key(self._path, name, str(value), quote_mode="never")
        logg.debug(f"{self._path} {name}={value}")

    def commented_var(self, name: str, value: Any):
        """
        Add env variables commented.
        """
        self.add_comment(f"{name}={value}")

    def add_comment(self, line: str):
        """
        Add comment line.
        """
        self.file.add_new_line(f"# {line}")
