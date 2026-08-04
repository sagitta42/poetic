from pathlib import Path

from poetic.settings import DotenvSettings
from poetic.setup.base import BaseSetup


class SettingsSetup(BaseSetup[DotenvSettings]):
    """
    Settings setup.

    Set up settings source file / class with pydantic-settings based class
        containing .env variables.
    """

    def __init__(self, settings: DotenvSettings, path: Path) -> None:
        super().__init__(settings, path)

    def setup(self, skip_super: bool = False) -> None:
        super().setup(skip_super)

        path_in_package = self.path
        if self._settings.package_subdir is not None:
            path_in_package = self.path / self._settings.package_subdir

        self._copy_template("settings.py", path_in_package=path_in_package)

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")
