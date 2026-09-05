from pathlib import Path

from poetiq.enums import ActionType
from poetiq.settings.setup import DotenvSettings
from poetiq.setup.base.poetry import BasePoetrySetup
from poetiq.utils.template import TemplateManager


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
        template_setup: ActionType | None = None,
        core: bool = True,
    ) -> None:
        super().__init__(path, settings, core)

        self._templates = TemplateManager(template_setup or self._type, self.path)

    def setup(self) -> None:
        """
        Set up Settings class / source file and a .env template.
        """
        super().setup()

        self._templates.copy(
            "settings.py", package_path=self.path / self._settings.subfolder
        )
        self.setup_dotenv_template()

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("pydantic_settings")
