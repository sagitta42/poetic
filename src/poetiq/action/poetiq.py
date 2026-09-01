from pathlib import Path

from poetiq.action.base import BaseAction
from poetiq.settings.base import T_Settings
from poetiq.utils.poetry import Poetry
from poetiq.utils.toml import TomlHandler


class PoetiqAction(BaseAction[T_Settings]):
    """
    Action that involves poetry and poetiq.toml
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        super().__init__(path, settings)

        self._toml_file = "poetiq.toml"
        self._poetiq_toml = TomlHandler(self.path / self._toml_file)
        self._poetiq_toml.read()

        self._poetry = Poetry(self.path)
