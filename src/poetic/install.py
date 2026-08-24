from functools import cached_property
from pathlib import Path

from pydantic import BaseModel

from poetic.exceptions import PoeticException
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

        if self._settings.package is None:
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
        for package_info in self._get_deps_of_interest():
            package_source = self._get_package_source(package_info.name)
            logg.debug(package_source)
            logg.debug(package_info.path)
            if message == "local" and not package_source == package_info.path:
                logg.info(
                    f"Replacing dual package {package_info.name} with {message} dependency",
                    header=True,
                )
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

    def _get_package_source(self, package: str) -> str | Path:
        """
        Get package install source from pip freeze.

        Source is be "python" if package version stated in pip freeze with "==".
        Source is path (git, local etc.) if version stated with "@".

        Get pip freeze command output and extract items containing package name.
        Check only items where package name corresponds to package (not contain it)
        """
        command_output = self.run(
            self.venv("pip"), "freeze", package, check=True, env=True
        )
        assert command_output is not None
        package_command_outputs = [cout for cout in command_output if package in cout]

        for package_output in package_command_outputs:
            if "@" in package_output:
                package_in_output, path = self._get_package_path(
                    package_output, prefix="file:"
                )
                if package_in_output != package:
                    continue

                return path

            try:
                package_in_output, version = self._get_package_info(
                    package_output, "=="
                )
                if package_in_output != package:
                    continue

                return version
            except Exception as e:
                raise e.__class__(
                    f"Impossible to extract package==version from string: {package_output}\nError: {e}"
                )

        raise PoeticException(f"Package {package} not found in pip freeze!")

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
            package, path = self._get_package_path(dep_str)
            ret.append(PackageInfo(name=package, path=path))
        return ret

    def _get_package_path(
        self, dep_str: str, prefix: str | None = None
    ) -> tuple[str, Path]:
        """
        Extract package name and path from "package @ path" dependency string.

        prefix: remove string from prefix of path string
        """
        package, path = self._get_package_info(dep_str, "@")

        if prefix is not None:
            path = path.removeprefix(prefix)

        return package, Path(path)

    def _get_package_info(self, dep_str: str, split_str: str) -> tuple[str, str]:
        """
        Get package information splitting dependency string by given split string.

        E.g. package==1.2.3, package @ path
        """
        package, info = [component.strip() for component in dep_str.split(split_str)]
        return package, info
