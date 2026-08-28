from pathlib import Path

from poetic.action.base import BaseAction
from poetic.settings.base import T_Settings
from poetic.utils.poetry import Poetry
from poetic.utils.toml import TomlHandler


class PoeticAction(BaseAction[T_Settings]):
    """
    Action that involves poetry and poetic.toml
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        super().__init__(path, settings)

        self._toml_file = "poetic.toml"
        self._poetic_toml = TomlHandler(self.path / self._toml_file)
        self._poetic_toml.read()

        self._poetry = Poetry(self.path)
