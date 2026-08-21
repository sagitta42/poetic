from functools import cached_property
from pathlib import Path

from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.venv import BaseVenvSetup
from poetic.utils.toml import PyProjectHandler, TomlHandler


class InstallSetup(BaseVenvSetup[InstallSettings]):
    """
    Install functionalities on top of standard poetry.

    Uses information in .poetic.toml file on dual dependencies.
    Checks information in pyproject.toml for install type.

    TODO: add local dependency to .poetic.toml with e.g. poetic install add
    TODO: reinstall only a specific given dual dependency, not all in .poetic.toml
    """

    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings)

        self._toml_file = ".poetic.toml"
        self._poetic_toml = TomlHandler(self.path / self._toml_file)
        self._pyproject = PyProjectHandler(self.path)

    def install(self):
        """
        Run poetry install handling dual dependencies.

        Determine if the --no-root flag is needed based on package mode in pyproject.toml

        If local flag was given in settings, perform local install:
            - perform poetry install
            - uninstall dual dependencies
            - install based on paths from .poetic.toml

        Otherwise perform install based on pyproject.toml:
            - uninstall dual dependencies
            - install based on pyproject.toml (i.e. standard poetry install)
        """
        if self._settings.local and not self._has_dual_deps():
            logg.warning(
                f"Local install requested but no dual dependencies found in {self._toml_file}"
            )

        if self._has_dual_deps() and not self._settings.local:
            # TODO: check if already points to pyproject and skip
            self._uninstall_dual_deps("pyproject.toml")

        poetry_args = ["install"]
        if not self._is_package_mode():
            poetry_args.append("--no-root")

        self.poetry(*poetry_args)

        if self._has_dual_deps() and self._settings.local:
            self._uninstall_dual_deps("local")
            # TODO: check if already points to local and skip
            for package, path in self._yield_dual_deps():
                self.pip("install", str(path))

    def _has_dual_deps(self) -> bool:
        """
        Determine if package has dual dependencies.
        """
        return len(self._dual_deps) > 0

    def _is_package_mode(self) -> bool:
        """
        Determine if current pyproject is in package mode.
        """
        project = self._pyproject.get_section("project")

        if "package-mode" not in project:
            return False

        return project["package-mode"]

    def _uninstall_dual_deps(self, message: str):
        """
        Uninstall dual dependencies.

        Uninstall dependencies listed as local in .poetic.toml
        """
        logg.info(f"Replacing dual packages with {message} dependencies", header=True)
        for package, _ in self._yield_dual_deps():
            self.pip("uninstall", package)

    def _yield_dual_deps(self):
        """
        Yield dual dependencies.

        Read dual dependencies.
        Extract and yield package name and path.
        """
        dual_deps = self._dual_deps
        for dep in dual_deps:
            package, path = [component.strip() for component in dep.split("@")]
            yield package, Path(path)

    @cached_property
    def _dual_deps(self) -> list[str]:
        """
        Get list of dual dependencies from poetic toml if stated.
        """
        poetic_settings = self._poetic_toml.get_section("poetic")
        ret = poetic_settings.get("local_dependencies", [])
        return ret
