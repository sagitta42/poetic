from pathlib import Path

from poetic.item.base import BaseDependencySetup
from poetic.settings.item import DotenvSettings


class EnvSettingsSetup(BaseDependencySetup[DotenvSettings]):
    """
    Environment Settings setup.

    Set up settings source file / class with pydantic-settings based class
        containing .env variables.
    """

    def __init__(self, settings: DotenvSettings, path: Path, core: bool) -> None:
        super().__init__(settings, path, core)

    def setup(self) -> None:
        super().setup()

        path_in_package = self.path
        if self._settings.package_subdir is not None:
            path_in_package = self.path / self._settings.package_subdir

        self._copy_template("settings.py", path_in_package=path_in_package)

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")
