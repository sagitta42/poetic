from pathlib import Path

from poetic.settings.item import DotenvSettings
from poetic.settings.setup import SetupType
from poetic.setup.poetry import BasePoetrySetup
from poetic.utils.template import TemplateManager


class EnvSettingsSetup(BasePoetrySetup[DotenvSettings]):
    """
    Environment Settings setup (pydantic-settings).

    Set up settings source file / class with pydantic-settings based class
        containing .env variables.
    """

    def __init__(
        self,
        path: Path,
        settings: DotenvSettings = DotenvSettings(),
        template_setup: SetupType | None = None,
        core: bool = True,
    ) -> None:
        super().__init__(path, settings, core)

        self._templates = TemplateManager(template_setup or self._type, self.path)

    def setup(self) -> None:
        """
        Set up Settings class / source file and a .env template.
        """
        super().setup()

        self._templates.copy("settings.py")
        self.setup_dotenv_template()

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")
