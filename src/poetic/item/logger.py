from pathlib import Path

from poetic.settings.item import LoggerSettings
from poetic.setup.dependency import BaseDependencySetup
from poetic.utils.files import replace_str_in_file
from poetic.utils.template import TemplateLocation


class LoggerSetup(BaseDependencySetup[LoggerSettings]):
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

        replace_str_in_file("POETIC_DEBUG", "DEBUG", path_in_package)

        self.setup_dotenv_template()

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("dotenv")
