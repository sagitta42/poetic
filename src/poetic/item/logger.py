from pathlib import Path

from poetic.settings.item import LoggerSettings
from poetic.setup.poetry import BasePoetrySetup
from poetic.utils.path import File
from poetic.utils.template import TemplateLocation


class LoggerSetup(BasePoetrySetup[LoggerSettings]):
    """
    Set up logger source file.
    """

    def __init__(
        self,
        path: Path,
        settings: LoggerSettings = LoggerSettings(),
        core: bool = False,
    ) -> None:
        super().__init__(path, settings, core)

    def setup(self) -> None:
        """
        Set up logger.py file.

        Copy poetic's own logger.py source file with Logger class into setup directory.
        Replace poetic's POETIC_DEBUG .env variable with the standard DEBUG for Logger debug mode.
        """
        super().setup()

        output_dir = self.path / self._settings.subfolder

        path_in_package = self._templates.copy(
            "logger.py",
            package_path=output_dir,
            template_location=TemplateLocation.poetic_src,
        )

        File(path_in_package).replace_str("POETIC_DEBUG", "DEBUG")

        self.setup_dotenv_template()

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("dotenv")
