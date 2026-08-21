from pathlib import Path

from poetic.settings.item import DotenvSettings
from poetic.setup.dependency import BaseDependencySetup


class EnvSettingsSetup(BaseDependencySetup[DotenvSettings]):
    """
    Environment Settings setup (pydantic-settings).

    Set up settings source file / class with pydantic-settings based class
        containing .env variables.
    """

    def __init__(
        self, path: Path, settings: DotenvSettings = DotenvSettings(), core: bool = True
    ) -> None:
        super().__init__(path, settings, core)

    def setup(self) -> None:
        """
        Set up Settings class / source file and a .env template.
        """
        super().setup()

        self._copy_template("settings.py")
        self.setup_dotenv_template()

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")

    def is_present(self) -> bool:
        """
        Check whether setup already present.

        Check if settings.py already exists
        """
        return self._package_file_exists("settings.py")
