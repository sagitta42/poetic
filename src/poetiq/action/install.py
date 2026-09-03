import enum
from functools import cached_property
from pathlib import Path
import subprocess


from poetiq.utils.poetry import Poetry
from poetiq.action.poetiq import PoetiqAction
from poetiq.exceptions import PoetiqException
from poetiq.settings.install import InstallSettings

from poetiq.logger import logg
from poetiq.utils.pip import PackageInfo, Pip, get_package_source


class InstallSource(str, enum.Enum):
    local = "local"
    pyproject = "pyproject"

    def __str__(self) -> str:
        return self.value


class InstallAction(PoetiqAction):
    """
    Install functionalities on top of standard poetry.

    Uses information in poetiq.toml file on dual dependencies.
    Checks information in pyproject.toml for install type.

    TODO: add local dependency to poetiq.toml with e.g. poetiq install add
    TODO: reinstall only a specific given dual dependency, not all in poetiq.toml
    """

    def __init__(self, path: Path, settings: InstallSettings) -> None:
        super().__init__(path, settings)

        self._pip = Pip(self.path)

    def launch(self):
        """
        Run poetry install handling dual dependencies.

        Determine if the --no-root flag is needed based on package mode in pyproject.toml.
        Run "poetry lock" automatically if poetry.lock determined to be too old.

        If local flag was given in settings, perform local install:
            - perform full poetry install if no specific package was requested
            - uninstall dual dependencies if they do not already point to local path
            - install based on paths from poetiq.toml

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
                self._pip.run("install", package.source, info=True)

    def _full_poetry_install(self):
        """
        Perform full poetry install.

        Add --no-root flag if not in package mode.
        """

        poetries = (
            self._get_split_poetries() if self._settings.split else [self._poetry]
        )

        for poetry in poetries:
            poetry_args = ["install"]

            if not poetry.is_package_mode():
                poetry_args.append("--no-root")

            logg.info(f"Installing from {poetry.path}...", poetiq=True)
            try:
                poetry.run(*poetry_args, check=True)
            except subprocess.CalledProcessError as e:
                if "poetry.lock" in e.stderr:
                    logg.info(f"-> Running poetry lock", poetiq=True)
                    poetry.run("lock")
                    poetry.run(*poetry_args, check=True)

    def _has_dual_packages(self) -> bool:
        """
        Determine if packages with dual dependencies are present.
        """
        return len(self._all_local_packages) > 0

    def _uninstall_dual_packages(self, install_source: InstallSource):
        """
        Uninstall dual packages.

        Uninstall dual packages of interest listed as local in poetiq.toml.
        Skip if package is not present in pip freeze.

        Local install: do not perform uninstall if package already points to same install path in pip freeze.
        Pyproject install: do not perform uninstall if package does NOT point to local path install source.
        """
        for local_package in self._get_local_packages_of_interest():
            pip_freeze_info = self._pip.get_package_info(local_package.name)

            if pip_freeze_info is None:
                continue

            assert (
                pip_freeze_info.source is not None
            ), "how is there no source in pip freeze"

            pip_source = pip_freeze_info.source.removeprefix("file://")

            if install_source == InstallSource.local:
                if local_package.source == pip_source:
                    continue
                logg.info(f"{pip_freeze_info.source} -> {local_package.source}")
            elif install_source == InstallSource.pyproject:
                # TODO: compare to actual pyproject
                if pip_source != local_package.source:
                    continue

            logg.info(
                f"Replacing dual package {local_package.name} with {install_source} dependency",
                header=True,
            )

            self._pip.run("uninstall", local_package.name, "-y", info=True)

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

    def _get_split_poetries(self) -> list[Poetry]:
        """
        Get list of poetry obejcts for each split pyproject.toml directory in poetiq.toml
        """
        poetiq_settings = self._poetiq_toml.get_section("dependency-groups")
        logg.debug(poetiq_settings)
        split_deps_dirs = poetiq_settings.get("split", [])
        logg.debug(split_deps_dirs)
        ret = [Poetry(self.path / dir, venv_path=self.path) for dir in split_deps_dirs]
        return ret

    @cached_property
    def _local_package_map(self) -> dict[str, PackageInfo]:
        ret = {package.name: package for package in self._all_local_packages}
        return ret

    @cached_property
    def _all_local_packages(self) -> list[PackageInfo]:
        """
        Get list of all local packages from poetiq toml.
        """
        poetiq_settings = self._poetiq_toml.get_section("dependency-groups")
        local_deps_items = poetiq_settings.get("local", [])
        ret = []
        for dep_str in local_deps_items:
            if not "@" in dep_str:
                raise PoetiqException(
                    f"Incorrect fromat in {self._toml_file} local dependency: {dep_str}! Use package @ path format"
                )
            package, path = get_package_source(dep_str)
            ret.append(PackageInfo(name=package, source=path, version=None))
        return ret
