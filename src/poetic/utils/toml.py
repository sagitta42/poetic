from pathlib import Path
import tomlkit
from typing import Any


class TomlHandler:
    def __init__(self, path_to_toml: Path):
        self._path = path_to_toml

        with open(self._path, "rb") as f:
            self._toml_dict_original = tomlkit.load(f)

        self._toml_dict = self._toml_dict_original.copy()

    def get_section(self, name: str) -> dict:
        return self._toml_dict[name]

    def add_section(self, name: str, items: dict[str, Any]):
        self._toml_dict[name] = items

    def del_section(self, name: str):
        self._toml_dict.pop(name)

    def save_toml(self):
        with open(self._path, "w") as f:
            tomlkit.dump(self._toml_dict, f)


class PyProjectHandler(TomlHandler):
    def __init__(self, path_to_pyproject: Path) -> None:
        super().__init__(path_to_pyproject / "pyproject.toml")
