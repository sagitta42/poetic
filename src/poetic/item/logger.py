from pathlib import Path
import shutil
from typing import Any

from poetic.settings.item import LoggerSettings
from poetic.setup.dependency import BaseDependencySetup


class LoggerSetup(BaseDependencySetup[LoggerSettings]):
    """
    Set up logger source file.
    """

    def __init__(
        self, path: Path, settings: LoggerSettings = LoggerSettings(), core: bool = True
    ) -> None:
        super().__init__(path, settings, core)

    def setup(self) -> None:
        """
        Set up logger.py file.

        Copy poetic's own logger.py source file with Logger class into setup directory.
        Replace poetic's POETIC_DEBUG .env variable with the standard DEBUG for Logger debug mode.
        """
        super().setup()

        output_dir = self.path
        if self._settings.subfolder is not None:
            output_dir = output_dir / self._settings.subfolder
        output_path = output_dir / "logger.py"

        shutil.copy(self._path_to_resources / "logger.py", output_path)
        self._replace_str_in_file("POETIC_DEBUG", "DEBUG", output_path)

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("dotenv")
