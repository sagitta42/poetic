from pathlib import Path

from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.venv import BaseVenvSetup


class InstallSetup(BaseVenvSetup[InstallSettings]):
    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings)

    def install(self):
        logg.info("To be implemented")
