from pathlib import Path

from poetic.settings import DotenvSettings
from poetic.setup.base import BaseSetup


class SettingsSetup(BaseSetup[DotenvSettings]):
    """
    Settings setup.
    """

    def __init__(self, settings: DotenvSettings, path: Path) -> None:
        super().__init__(settings, path)

    def setup(self) -> None:
        super().setup()

        self._copy_template("settings.py", generic=True)

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")