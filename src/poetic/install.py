from pathlib import Path

from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.venv import BaseVenvSetup
from poetic.utils.toml import TomlHandler


class InstallSetup(BaseVenvSetup[InstallSettings]):
    """
    Install functionalities on top of standard poetry.

    TODO: add local dependency to .poetic.toml with e.g. poetic install add
    """

    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings)

        self._toml_handler = TomlHandler(self.path / ".poetic.toml")

    def install(self):
        """
        Run install.

        Run standard poetry install.
        If local flag was given in settings, perform local install based on .poetic.cfg
        """

        self._run(self.venv("poetry"), "install", env=True)

        if self._settings.local:
            poetic_settings = self._toml_handler.get_section("poetic")
            dependencies = poetic_settings["local_dependencies"]
            # TODO: check if already points to local and skip
            for dep in dependencies:
                package, path = [component.strip() for component in dep.split("@")]
                logg.info(f"Replacing {package} with local dependency", header=True)
                self.pip("uninstall", package)
                logg.info(f"Installing local {package} @ {path}")
                self.pip("install", path)
            logg.info(f"To be implemented: {dependencies}")
