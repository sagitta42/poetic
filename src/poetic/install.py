from functools import cached_property
from pathlib import Path

from pydantic import BaseModel

from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.venv import BaseVenvSetup
from poetic.utils.toml import PyProjectHandler, TomlHandler


class PackageInfo(BaseModel):
    name: str
    path: Path


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

        Perform dual package treatment on given package name; or all if none are given.
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
            for pacakge_info in self._get_deps_of_interest():
                self.pip("install", str(pacakge_info.path))

    def _has_dual_deps(self) -> bool:
        """
        Determine if package has dual dependencies.
        """
        return len(self._all_dual_deps) > 0

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

        Uninstall dependencies of interest listed as local in .poetic.toml
        """
        logg.info(f"Replacing dual packages with {message} dependencies", header=True)
        for package_info in self._get_deps_of_interest():
            self.pip("uninstall", package_info.name)

    def _get_deps_of_interest(self) -> list[PackageInfo]:
        """
        Get list of dependencies of interest.

        All dependencies if no specific package requested.
        """

        ret = (
            [self._dual_deps_map[self._settings.package]]
            if self._settings.package is not None
            else self._all_dual_deps
        )
        return ret

    @cached_property
    def _dual_deps_map(self) -> dict[str, PackageInfo]:
        ret = {package_info.name: package_info for package_info in self._all_dual_deps}
        return ret

    @cached_property
    def _all_dual_deps(self) -> list[PackageInfo]:
        """
        Get list of all dual dependencies from poetic toml.
        """
        poetic_settings = self._poetic_toml.get_section("poetic")
        local_deps_items = poetic_settings.get("local_dependencies", [])
        ret = []
        for dep_str in local_deps_items:
            package, path = [component.strip() for component in dep_str.split("@")]
            ret.append(PackageInfo(name=package, path=path))
        return ret
