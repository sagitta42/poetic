from pathlib import Path
import venv

from pydantic import BaseModel

from poetic.command_runner import BaseCommandRunner
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.pip import get_package_source, get_package_version
from poetic.utils.utils import list_as_args


class PackageInfo(BaseModel):
    name: str
    version: str | None
    source: str | None


class BaseVenvSetup(BaseFunctionalitySetup[T_Settings], BaseCommandRunner):
    """
    General functionality setup with venv.

    Includes additional operations: venv setup
    """

    def __init__(self, path: Path, settings: T_Settings) -> None:
        BaseFunctionalitySetup.__init__(self, path, settings)
        BaseCommandRunner.__init__(self, path)

        self._path_to_venv = (self.path / "venv").resolve()

    def setup(self) -> None:
        """
        Main setup.

        In addition to previous setup: set up venv.
        """
        super().setup()

        if not self._path_to_venv.exists():
            logg.info("...creating venv", header=True)
            venv.create(self._path_to_venv, with_pip=True)

    def venv(self, exe: str) -> Path:
        """
        Get venv path to executable.
        """
        ret = self._path_to_venv / "bin" / exe
        return ret

    def pip(self, *args):
        """
        Run a pip command in project's venv.
        """
        self._venv_command("pip", *args, env=True)

    def _venv_command(self, command: str, *args, env: bool = False):
        """
        Run a venv-based command with given arguments.

        Invoke path/to/venv/command.
        """
        logg.info(f"poetic: {command} {list_as_args(args)}", header=True)
        self.run(self.venv(command), *args, env=env)

    def _get_pip_package_info(self, name: str) -> PackageInfo | None:
        """
        Get info of pip package, if present in pip freeze.
        """
        all_pip_packages = self._get_all_pip_packages()
        for package in all_pip_packages:
            if package.name == name:
                return package

        return None

    def _get_all_pip_packages(self) -> list[PackageInfo]:
        """
        Get package infos from pip freeze.

        Version if package==1.2.3.
        Path if package @ path (preserves file:// prefix)
        """
        pip_packages = self._get_pip_freeze_info()

        ret = []
        for package_info in pip_packages:
            if "@" in package_info:
                name, source = get_package_source(package_info)
                version = None
            elif "==" in package_info:
                name, version = get_package_version(package_info)
                source = None
            else:
                raise NotImplementedError(
                    f"Could not parse pip freeze format {package_info}! Checking for @ or ==; unrecognized"
                )

            ret.append(PackageInfo(name=name, version=version, source=source))

        return ret

    def _get_pip_freeze_info(self) -> list[str]:
        """
        Get output of pip freeze in list format.
        """
        ret = self.run(self.venv("pip"), "freeze", check=True, env=True)
        assert ret is not None
        return ret
