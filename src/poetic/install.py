from pathlib import Path

from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.venv import BaseVenvSetup


class InstallSetup(BaseVenvSetup[InstallSettings]):
    """
    Install functionalities on top of standard poetry.
    """

    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings)

    def install(self):
        """
        Run install.

        Run standard poetry install.
        If local flag was given in settings, perform local install based on .poetic.cfg
        """

        self._run(self.venv("poetry"), "install", env=True)

        if self._settings.local:
            logg.info("To be implemented")
