import enum
from functools import cached_property
from pathlib import Path


from poetic.exceptions import PoeticException
from poetic.settings.install import InstallSettings

from poetic.logger import logg
from poetic.setup.dependency import BaseDependencySetup
from poetic.setup.venv import PackageInfo
from poetic.utils.pip import get_package_source
from poetic.utils.toml import PyProjectHandler, TomlHandler


class InstallSource(str, enum.Enum):
    local = "local"
    pyproject = "pyproject"

    def __str__(self) -> str:
        return self.value


class InstallSetup(BaseDependencySetup[InstallSettings]):
    """
    Install functionalities on top of standard poetry.

    Uses information in .poetic.toml file on dual dependencies.
    Checks information in pyproject.toml for install type.

    TODO: add local dependency to .poetic.toml with e.g. poetic install add
    TODO: reinstall only a specific given dual dependency, not all in .poetic.toml
    """

    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings, core=False)

        self._toml_file = "poetic.toml"
        self._poetic_toml = TomlHandler(self.path / self._toml_file)
        self._poetic_toml.read()

        self._pyproject = PyProjectHandler(self.path)
        self._pyproject.read()

    def install(self):
        """
        Run poetry install handling dual dependencies.

        Determine if the --no-root flag is needed based on package mode in pyproject.toml.

        If local flag was given in settings, perform local install:
            - perform full poetry install if no specific package was requested
            - uninstall dual dependencies if they do not already point to local path
            - install based on paths from .poetic.toml

        Otherwise perform install based on pyproject.toml:
            - uninstall dual dependencies
                TODO: check if already points to pyproject and skip
            - install based on pyproject.toml (i.e. standard poetry install)

        Perform dual package treatment on given package name; or all if none are given.
        """
        if self._settings.local and not self._has_dual_packages():
            logg.warning(
                f"Local install requested but no dual dependencies found in {self._toml_file}"
            )

        if self._has_dual_packages() and not self._settings.local:
            self._uninstall_dual_packages(InstallSource.pyproject)

        if self._settings.package == "":
            self._full_poetry_install()

        if self._has_dual_packages() and self._settings.local:
            self._uninstall_dual_packages(InstallSource.local)
            for package in self._get_local_packages_of_interest():
                self.pip("install", package.source)

    def _full_poetry_install(self):
        """
        Perform full poetry install.

        Add --no-root flag if not in package mode.
        """
        poetry_args = ["install"]
        if not self._is_package_mode():
            poetry_args.append("--no-root")

        self.poetry(*poetry_args)

    def _has_dual_packages(self) -> bool:
        """
        Determine if packages with dual dependencies are present.
        """
        return len(self._all_local_packages) > 0

    def _is_package_mode(self) -> bool:
        """
        Determine if current pyproject is in package mode.
        """
        project = self._pyproject.get_section("project")

        if "package-mode" not in project:
            return False

        return project["package-mode"]

    def _uninstall_dual_packages(self, install_source: InstallSource):
        """
        Uninstall dual packages.

        Uninstall dual packages of interest listed as local in .poetic.toml.
        Skip if package is not present in pip freeze.

        Local install: do not perform uninstall if package already points to same install path in pip freeze.
        Pyproject install: do not perform uninstall if package does NOT point to local path install source.
        """
        for local_package in self._get_local_packages_of_interest():
            pip_freeze_info = self._get_pip_package_info(local_package.name)

            if pip_freeze_info is None:
                continue

            assert (
                pip_freeze_info.source is not None
            ), "how is there no source in pip freeze"

            pip_source = pip_freeze_info.source.removeprefix("file://")
            logg.debug(pip_freeze_info.source)
            logg.debug(pip_source)

            if install_source == InstallSource.local:
                if local_package.source == pip_source:
                    continue
            elif install_source == InstallSource.pyproject:
                if local_package.source != pip_source:
                    continue

            logg.info(
                f"Replacing dual package {local_package.name} with {install_source} dependency:",
                header=True,
            )
            logg.info(f"{pip_freeze_info.source} -> {local_package.source}")

            self.pip("uninstall", local_package.name, "-y")

    def _get_local_packages_of_interest(self) -> list[PackageInfo]:
        """
        Get list of local packages of interest for install.

        All local packages if no specific package requested.
        """

        ret = (
            [self._local_package_map[self._settings.package]]
            if self._settings.package != ""
            else self._all_local_packages
        )
        return ret

    @cached_property
    def _local_package_map(self) -> dict[str, PackageInfo]:
        ret = {package.name: package for package in self._all_local_packages}
        return ret

    @cached_property
    def _all_local_packages(self) -> list[PackageInfo]:
        """
        Get list of all local packages from poetic toml.
        """
        poetic_settings = self._poetic_toml.get_section("dependency-groups")
        local_deps_items = poetic_settings.get("local", [])
        ret = []
        for dep_str in local_deps_items:
            if not "@" in dep_str:
                raise PoeticException(
                    f"Incorrect fromat in {self._toml_file} local dependency: {dep_str}! Use package @ path format"
                )
            package, path = get_package_source(dep_str)
            ret.append(PackageInfo(name=package, source=path, version=None))
        return ret
