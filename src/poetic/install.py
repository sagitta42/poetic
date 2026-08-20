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
        Run poetry install handling dual dependencies.

        If local flag was given in settings, perform local install:
            - uninstall dual dependencies
            - install based on paths from .poetic.toml

        Otherwise perform install based on pyproject.toml
        """

        if not self._settings.local:
            # TODO: check if already points to pyproject and skip
            self._uninstall_dual_deps("pyproject.toml")

        self._run(self.venv("poetry"), "install", env=True)

        if self._settings.local:
            self._uninstall_dual_deps("local")
            # TODO: check if already points to local and skip
            for package, path in self._yield_dual_deps():
                logg.info(f"Installing local {package} @ {path}")
                self.pip("install", str(path))

    def _uninstall_dual_deps(self, message: str):
        """
        Uninstall dual dependencies.

        Uninstall dependencies listed as local in .poetic.toml
        """
        logg.info(f"Replacing dual packages with {message} dependencies", header=True)
        for package, _ in self._yield_dual_deps():
            self.pip("uninstall", package)

    def _yield_dual_deps(self):
        dual_deps = self._get_dual_deps()
        for dep in dual_deps:
            package, path = [component.strip() for component in dep.split("@")]
            yield package, Path(path)

    def _get_dual_deps(self) -> list[str]:
        """
        Get list of dual dependencies from poetic toml if stated.
        """
        poetic_settings = self._poetic_toml.get_section("poetic")
        ret = poetic_settings.get("local_dependencies", [])
        return ret
