from abc import abstractmethod
import os
from pathlib import Path
import venv

from poetic.command_runner import BaseCommandRunner
from poetic.logger import logg
from poetic.settings.base import T_Settings
from poetic.setup.functionality import BaseFunctionalitySetup
from poetic.utils.utils import list_as_args


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
