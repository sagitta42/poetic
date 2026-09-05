from pathlib import Path


from poetiq.settings.base import T_SetupSettings
from poetiq.setup.base.functionality import BaseFunctionalitySetup
from poetiq.utils.venv import Venv


class BaseVenvSetup(BaseFunctionalitySetup[T_SetupSettings]):
    """
    General functionality setup with pip and venv.
    """

    def __init__(
        self, path: Path | None, settings: T_SetupSettings, core: bool
    ) -> None:
        super().__init__(path, settings, core)

        self._venv = Venv(self.path)

    def setup(self) -> None:
        """
        Main setup.

        In addition to previous setup: set up venv.
        """
        super().setup()

        self._venv.setup()
        self._gitignore_file.add_new_line("venv/")
