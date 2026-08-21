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
        Copy poetic's own logger.py source file with Logger class into setup directory.
        """
        super().setup()

        shutil.copy(self._path_to_resources / "logger.py", self.path / "logger.py")

    def setup_dependencies(self) -> None:
        super().setup_dependencies()

        self._poetry_add("dotenv")
