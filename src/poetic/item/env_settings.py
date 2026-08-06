from pathlib import Path

from poetic.settings.item import DotenvSettings
from poetic.setup.dependency import BaseDependencySetup


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

        self._copy_template("settings.py")

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")

    def is_present(self) -> bool:
        """
        Check whether setup already present.

        Check if settings.py already exists
        """
        return self._package_file_exists("settings.py")
