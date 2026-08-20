from pathlib import Path
import tomlkit
from typing import Any


class TomlHandler:
    """
    Toml file handler.

    path_to_toml (Path): path to .toml file

    Functionalities to read/save file and get/add/delete sections.
    If file does not exist, treat it as empty toml.
    """

    def __init__(self, path_to_toml: Path):
        self._path = path_to_toml

        if self._path.exists():
            with open(self._path, "rb") as f:
                self._toml_dict_original = tomlkit.load(f)
        else:
            self._toml_dict_original = {}

        self._toml_dict = self._toml_dict_original.copy()

    def get_section(self, name: str) -> dict:
        """
        Get section of given name.

        If does not exist, treat it as empty section.
        """
        return self._toml_dict.get(name, {})

    def add_section(self, name: str, items: dict[str, Any]):
        self._toml_dict[name] = items

    def del_section(self, name: str):
        self._toml_dict.pop(name)

    def save_toml(self):
        with open(self._path, "w") as f:
            tomlkit.dump(self._toml_dict, f)


class PyProjectHandler(TomlHandler):
    """
    Toml handler for pyproject.toml.

    path (Path): path to directory containing pyproject.toml
    """

    def __init__(self, path: Path) -> None:
        super().__init__(path / "pyproject.toml")
