from pathlib import Path


from poetic.settings.setup import T_SetupSettings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.venv import Venv


class BaseVenvSetup(BaseFunctionalitySetup[T_SetupSettings]):
    """
    General functionality setup with pip and venv.
    """

    def __init__(self, path: Path, settings: T_SetupSettings, core: bool) -> None:
        BaseFunctionalitySetup.__init__(self, path, settings, core)

        self._venv = Venv(self.path)

    def setup(self) -> None:
        """
        Main setup.

        In addition to previous setup: set up venv.
        """
        super().setup()

        self._venv.setup()
        self._gitignore_file.add_new_line("venv/")
