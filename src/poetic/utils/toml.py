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

        self._toml_dict_original: dict | None = None
        self._toml_dict: dict = {}

    def get_section(self, name: str) -> dict:
        """
        Get section of given name.

        If does not exist, treat it as empty section.
        Interpret composite section name iteratively (e.g. tool.poetic)
        """
        if "." in name:
            super_section, inner_section = name.split(".")
            return self.get_section(super_section).get(inner_section, {})

        return self._toml_dict.get(name, {})

    def add_section(self, name: str, items: dict[str, Any]):
        """
        Add items to given section.

        Create section if does not exist.
        Set given items in the section (will overwrite existing).
        Interpret composite section name iteratively (e.g. tool.poetic)
        """
        if "." in name:
            super_section, inner_section = name.split(".")
            self.add_section(super_section, items={inner_section: items})
            return

        if name not in self._toml_dict:
            self._toml_dict[name] = {}

        self._toml_dict[name] |= items

    def del_section(self, name: str):
        """
        Remove section if exists.
        """
        if name in self._toml_dict:
            self._toml_dict.pop(name)

    def save_toml(self):
        with open(self._path, "w") as f:
            tomlkit.dump(self._toml_dict, f)

    def read(self):
        """
        Read original .toml.

        If .toml has not yet been read, read .toml in path.
        Otherwise raise error about the second read.
        It is supposed to be read only once, and changes kept track in class.
        """
        if self._toml_dict_original is not None:
            raise RuntimeError(f"{self._path} has already been read!")
        if self._path.exists():
            with open(self._path, "rb") as f:
                self._toml_dict_original = tomlkit.load(f)
        else:
            self._toml_dict_original = {}

        self._toml_dict = self._toml_dict_original.copy()


class PyProjectHandler(TomlHandler):
    """
    Toml handler for pyproject.toml.

    path (Path): path to directory containing pyproject.toml
    """

    def __init__(self, path: Path) -> None:
        super().__init__(path / "pyproject.toml")
